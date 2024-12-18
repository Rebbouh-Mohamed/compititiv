from django.contrib import admin
from .models import *
# Register your models here.
class AdminContestParticipation(admin.ModelAdmin):
    ordering=("-pionts",)

admin.site.register(Contest)
admin.site.register(ContestParticipation,AdminContestParticipation)
