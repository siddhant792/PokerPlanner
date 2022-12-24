from django.contrib.auth.models import AnonymousUser

from channels.middleware import BaseMiddleware

from apps.user.models import Token


def get_user(token_key):
    """
    Gets user from a token_key
    """
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    """
    TokenAuthMiddleware to add user object to scope in websockets
    """

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((query.split('=') for query in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else get_user(token_key)
        return await super().__call__(scope, receive, send)
