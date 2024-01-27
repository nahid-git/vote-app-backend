from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.manager import AccountManager


class Account(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(max_length=100, unique=True)
    student_id = models.CharField(max_length=16)
    name = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.email


class EmailConfirmationModel(models.Model):
    uid = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=1000)

    def __str__(self):
        return self.token


class ForgotPasswordModel(models.Model):
    uid = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=1000)

    def __str__(self):
        return self.token
