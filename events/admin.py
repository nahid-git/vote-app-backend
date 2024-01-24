from django.contrib import admin

from events.models import Event, Vote


# Register your models here.

class VoteAdmin(admin.TabularInline):
    model = Vote
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = [
        VoteAdmin
    ]
    list_display = ('title', 'description', 'created_at', 'updated_at', 'expired_at')


admin.site.register(Event, EventAdmin)
