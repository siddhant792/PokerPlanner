from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from apps.group import (
    models as group_models,
    permissions as group_permissions,
    serializer as group_serializers,
)


class GroupViewset(ModelViewSet):
    """
    Group API for creating group and get list of groups a user is associated with.
    """
    serializer_class = group_serializers.GroupSerializer

    def perform_create(self, serializer):
        """
        Saves serializer and injects created_by property as current user
        """
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        """
        Gets groups list in which current user is a member.
        """
        return group_models.Group.objects.filter(members__user=self.request.user)


class GroupMemberApi(CreateAPIView):
    """
    Group user API for adding group member
    """
    serializer_class = group_serializers.AddGroupMemberSerializer
    permission_classes = [group_permissions.IsGroupAdminPermission]

    def perform_create(self, serializer):
        """
        Adds a member to group, checks current user permission.
        """
        group = serializer.validated_data["group"]
        self.check_object_permissions(self.request, group)
        serializer.save()
