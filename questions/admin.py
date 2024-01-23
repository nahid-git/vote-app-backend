from django.contrib import admin

from questions.models import Question


# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'created_at', 'updated_at')


admin.site.register(Question, QuestionAdmin)
