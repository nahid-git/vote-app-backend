from django.db import models

from authentication.models import Account


# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(null=True)
    accounts = models.ManyToManyField(Account, through='Vote')

    def __str__(self):
        return self.title


class Vote(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'account')


class VoterSelectedOption(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='voterselectedoption')
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)
    selected_option = models.ForeignKey('options.Option', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vote', 'question')
