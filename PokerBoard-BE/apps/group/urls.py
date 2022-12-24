from django.urls import path

from rest_framework import routers

from apps.group import views as group_views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', group_views.GroupViewset, basename="groups")

urlpatterns = [
    path('create-members', group_views.GroupMemberApi.as_view(), name="create-members")
] + router.urls
