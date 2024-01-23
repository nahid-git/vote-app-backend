from django.contrib import admin

from options.models import Option


# Register your models here.

class OptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question', 'created_at', 'updated_at')


admin.site.register(Option, OptionAdmin)
