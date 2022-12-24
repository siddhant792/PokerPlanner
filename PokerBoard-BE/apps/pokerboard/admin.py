from django.contrib import admin

from apps.pokerboard import models as pokerboard_models

admin.site.register(pokerboard_models.Pokerboard)
admin.site.register(pokerboard_models.Ticket)
admin.site.register(pokerboard_models.GameSession)
admin.site.register(pokerboard_models.Vote)
admin.site.register(pokerboard_models.Invite)
