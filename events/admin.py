from django.contrib import admin

from events.models import Event
from votes.admin import VoteAdmin


# Register your models here.

class EventAdmin(admin.ModelAdmin):
    inlines = [
        VoteAdmin
    ]
    list_display = ('title', 'description', 'created_at', 'updated_at', 'expired_at')


admin.site.register(Event, EventAdmin)
