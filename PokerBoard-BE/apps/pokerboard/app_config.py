from django.apps import AppConfig
from django.db.models.signals import post_save

class PokerboardConfig(AppConfig):
    """
    Pokerboard application configuration
    """
    name = 'apps.pokerboard'

    def ready(self) -> None:
        from apps.pokerboard.signals import send_email_handler
        from apps.pokerboard.models import Invite
        post_save.connect(send_email_handler, sender=Invite)
