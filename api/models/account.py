from django.db import models
from django.utils import timezone

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE, related_name='accounts')