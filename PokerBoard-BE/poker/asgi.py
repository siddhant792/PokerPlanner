from django.urls import path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from apps.pokerboard.consumers import SessionConsumer
from poker.token_auth import TokenAuthMiddleware

ws_patterns = [
    path("session/<int:pk>", SessionConsumer.as_asgi())
]

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": TokenAuthMiddleware(URLRouter(ws_patterns)),
})
