from django.contrib import admin
from .models import Team, Profile, Round, Evidence, Answer

# Register your models here.
admin.site.register(Team)
admin.site.register(Profile)
admin.site.register(Round)
admin.site.register(Evidence)
admin.site.register(Answer)