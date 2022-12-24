from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.group import models as group_models
from apps.user import (
    models as user_models,
    serializers as user_serializers
)


class GroupMemberSerializer(serializers.ModelSerializer):
    """
    Group serializer for adding group members
    """
    user = user_serializers.UserSerializer()

    class Meta:
        model = group_models.GroupMember
        fields = ['id', 'user', 'group', 'created_at', 'updated_at']


class AddGroupMemberSerializer(serializers.Serializer):
    """
    Serializer for adding group member
    """
    user = user_serializers.UserSerializer(read_only=True)
    email = serializers.EmailField(write_only=True)
    group = serializers.PrimaryKeyRelatedField(queryset=group_models.Group.objects.only("id"))

    def validate(self, attrs):
        """
        Checks if user with given email exists or not.
        If exists, check if the user has already been added to the group.
        """
        email = attrs["email"]
        group = attrs["group"]
        user = get_user_model().objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("No such user")
        member = group_models.GroupMember.objects.filter(user=user, group=group).count()
        if member > 0:
            raise serializers.ValidationError("A member can't be added to a group twice")
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """
        Creates group user object
        """
        group = validated_data["group"]
        user = validated_data["user"]
        instance = group_models.GroupMember.objects.create(user=user, group=group)
        return instance


class GroupSerializer(serializers.ModelSerializer):
    """
    Group serializer fetching/adding groups
    """

    members = GroupMemberSerializer(many=True, read_only=True)

    class Meta:
        model = group_models.Group
        fields = ['id', 'name', 'members', 'created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'created_by': {
                'read_only': True,
            },
        }
