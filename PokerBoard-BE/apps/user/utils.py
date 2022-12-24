import datetime

from django.conf import settings


def get_expire_date():
    """
    Generating expiry date for token
    """
    return datetime.datetime.now() + datetime.timedelta(minutes=settings.TOKEN_TTL)
