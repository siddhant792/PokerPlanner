from django.urls import path

from apps.user import views


urlpatterns = [
    path('register', views.RegisterApiView.as_view(), name='register'),
    path('activate/<slug:pk>', views.ActivateAccountView.as_view(), name='activate'),
    path('login', views.LoginView.as_view(), name='login'),
    path('user/<slug:pk>', views.UserProfileView.as_view(), name='user'),
]
