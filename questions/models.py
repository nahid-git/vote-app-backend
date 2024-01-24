from django.db import models

from events.models import Event
from options.models import Option


class Question(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, related_name='questions', on_delete=models.CASCADE)
    options = models.ManyToManyField(Option, related_name='options')

    def __str__(self):
        return self.title
