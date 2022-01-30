from django.contrib import admin
from .models import (
    Team,
    Profile,
    Round,
    Evidence,
    Answer,
    Notification,
    Universal,
    Killcode,
)

# Register your models here.
admin.site.register(Team)
admin.site.register(Profile)
admin.site.register(Round)
admin.site.register(Evidence)
admin.site.register(Answer)
admin.site.register(Notification)
admin.site.register(Universal)
admin.site.register(Killcode)
