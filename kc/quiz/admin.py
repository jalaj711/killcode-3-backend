from django.contrib import admin
from .models import (
    Team,
    Profile,
    Round,
    Evidence,
    Answer,
    Universal,
    Killcode,
    ClueRedirect
)

# class AnswerInline(admin.StackedInline):
#     model=Answer
#     extra=3

class RoundAdmin(admin.ModelAdmin):
    # fields=['round_no','riddle','killer_msg','ca','ca_location','ca_victim','tries','start_time','end_time']
    # inlines=[AnswerInline]
    list_display = ("round_no","start_time", "end_time")

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("team_name", "participant1","participant1_phone","participant2","participant2_phone","participant3","participant3_phone","participant4","participant4_phone")




# Register your models here.
#admin.site.register(Team)
admin.site.register(Profile)
admin.site.register(Round)
admin.site.register(Evidence)
admin.site.register(Answer)
admin.site.register(Universal)
admin.site.register(Killcode)
admin.site.register(ClueRedirect)
