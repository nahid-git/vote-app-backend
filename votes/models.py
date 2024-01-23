from django.db import models

from authentication.models import Account
from events.models import Event


# Create your models here.

class Vote(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
