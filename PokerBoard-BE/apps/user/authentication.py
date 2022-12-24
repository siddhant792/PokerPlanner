import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.user import models as user_models


class CustomTokenAuthentication(TokenAuthentication):
    """
    Checking if the token has expired
    """
    model = user_models.Token

    def authenticate_credentials(self, key):
        """
        Check if the token is valid with the provided key
        """
        user, token = super().authenticate_credentials(key)
        if token.expired_at < datetime.datetime.now():
            raise AuthenticationFailed({"error": "Token has expired"})
        return user, token
