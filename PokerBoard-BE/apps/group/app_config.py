from django.apps import AppConfig
from django.db.models.signals import post_save


class GroupConfig(AppConfig):
    name = 'apps.group'

    def ready(self) -> None:
        """
        Registers a signal at the start of app
        """
        from apps.group.models import Group
        from apps.group.signals import create_default_group_member
        post_save.connect(create_default_group_member, sender=Group)
