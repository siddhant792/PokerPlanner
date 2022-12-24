from django.core import exceptions
from django.contrib.auth import authenticate, hashers
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers as rest_framework_serializers

from apps.user import(
    constants as user_constants,
    models as user_models,
)

from apps.group import models as group_models
from apps.pokerboard import models as pokerboard_models


class UserSerializer(rest_framework_serializers.ModelSerializer):
    """
    Custom User Serializer class
    """
    class Meta:
        model = user_models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self, **kwargs):
        if 'password' in self.validated_data:
            self.validated_data['password'] = hashers.make_password(self.validated_data['password'])
        return super().save(**kwargs)


class AccountVerificationSerializer(rest_framework_serializers.Serializer):
    """
    Email verification serializer
    """
    token = rest_framework_serializers.CharField(max_length=150, write_only=True)

    def validate_token(self, attrs):
        """
        Checking if the token is valid for account activation
        """
        account_activation_token = PasswordResetTokenGenerator()
        if account_activation_token.check_token(self.instance, attrs):
            return self.instance
        raise rest_framework_serializers.ValidationError(user_constants.EMAIL_VALIDATION_ERROR)

    def update(self, user, validated_data):
        """
        Activating user's account
        """
        user.is_account_verified = True
        user.save(update_fields=["is_account_verified"])
        return user


class LoginSerializer(rest_framework_serializers.Serializer):
    """
    Validating login credentials
    """
    email = rest_framework_serializers.EmailField()
    password = rest_framework_serializers.CharField()

    def validate(self, attrs):
        """
        Validating if user exists with given credentials
        """
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if not user.is_active:
                raise exceptions.ValidationError('User account is disabled.')
            if not user.is_account_verified:
                raise exceptions.ValidationError('Please activate your account.')
        else:
            raise exceptions.ValidationError('Unable to log in with provided credentials.')

        attrs['user'] = user
        return attrs


class UserTokenSerializer(UserSerializer):
    """
    Generating token for already registered user
    """
    token = rest_framework_serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['token']

    def get_token(self, user):
        """
        Creating token for already registered user
        """
        return user_models.Token.objects.create(user=user).key


class UserProfileSerializer(rest_framework_serializers.ModelSerializer):
    """
    User Profile Serializer
    """
    pokerboard = rest_framework_serializers.SerializerMethodField()
    group = rest_framework_serializers.SerializerMethodField()
    vote = rest_framework_serializers.SerializerMethodField()

    class Meta:
        model = user_models.User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'pokerboard', 'group', 'vote'
        ]

    def get_pokerboard(self, user):
        from apps.pokerboard.serializers import PokerboardSerializer

        boardquery = pokerboard_models.Pokerboard.objects.filter(
            manager=user
        ).prefetch_related("tickets")
        invites = pokerboard_models.Pokerboard.objects.filter(
            invite__invitee=user, invite__is_accepted=True
        )
        return PokerboardSerializer(boardquery.union(invites), many=True).data

    def get_vote(self, user):
        from apps.pokerboard.serializers import TicketSerializer

        tickets = pokerboard_models.Ticket.objects.filter(
            estimations__votes__user=user
        ).exclude(estimate=None).distinct()
        return TicketSerializer(tickets, many=True).data

    def get_group(self, user):
        from apps.group import serializer as group_serializers

        groups = group_models.Group.objects.filter(members__user=user)
        return group_serializers.GroupSerializer(groups, many=True).data
