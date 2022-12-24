from django.contrib import admin

from apps.group import models as group_models


admin.site.register(group_models.Group)
admin.site.register(group_models.GroupMember)
