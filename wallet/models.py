from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Wallet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="balance")
    balance = models.IntegerField(default = 0)


class Transaction(models.Model):
    sender = models.CharField(max_length=255, null=True)
    receiver = models.CharField(max_length=255, null=True)
    amount=models.IntegerField(default = 0)
    timestamp = models.DateTimeField(max_length=255, null=True)

