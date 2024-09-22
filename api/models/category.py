from django.db import models
from django.utils import timezone

from api.utils import set_timezone_aware_dates

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE, related_name='categories')

    # Track the month using a DateField, defaulting to the first day of the current month
    date = models.DateTimeField(default=timezone.now)

    budget = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        set_timezone_aware_dates(self, self.user)

        super(Category, self).save(*args, **kwargs)