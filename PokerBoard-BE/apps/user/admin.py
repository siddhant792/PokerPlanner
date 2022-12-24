from django.contrib import admin

from apps.user import models as user_models


admin.site.register(user_models.User)
admin.site.register(user_models.Token)
