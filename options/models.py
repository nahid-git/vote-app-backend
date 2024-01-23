from django.db import models

from questions.models import Question


# Create your models here.

class Option(models.Model):
    title = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title