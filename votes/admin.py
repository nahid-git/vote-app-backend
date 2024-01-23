from django.contrib import admin

from votes.models import Vote


# Register your models here.

class VoteAdmin(admin.TabularInline):
    model = Vote
    extra = 1