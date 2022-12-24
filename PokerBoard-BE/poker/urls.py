from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('groups/', include('apps.group.urls')),
    path('accounts/', include('apps.user.urls')),
    path('pokerboards/', include('apps.pokerboard.urls')),
]
