from os import name
from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.pokerboard import views as pokerboard_views

router = SimpleRouter(trailing_slash=False)
router.register('members', pokerboard_views.PokerboardMembersApiView, basename="members")
router.register('game', pokerboard_views.GameSessionApi, basename="game-session")
router.register('',pokerboard_views.PokerboardApiView, basename="pokerboards")

urlpatterns = [
    path("votes", pokerboard_views.VoteApiView.as_view(), name="votes"),
    path("jql", pokerboard_views.JqlAPIView.as_view(), name="jql"),
    path("comment", pokerboard_views.CommentApiView.as_view(), name="comment"),
    path("suggestions", pokerboard_views.SuggestionsAPIView.as_view(), name="suggestions"),
    path("<int:pk>/order-tickets", pokerboard_views.TicketOrderApiView.as_view(), name="order-tickets"),
] + router.urls
