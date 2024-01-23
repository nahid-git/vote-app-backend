from django.db import models

from events.models import Event


# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
