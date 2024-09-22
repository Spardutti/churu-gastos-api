from django.db import models
from django.utils import timezone

from api.utils import set_timezone_aware_dates

class UniqueExpense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        set_timezone_aware_dates(self, self.user)

        super(UniqueExpense, self).save(*args, **kwargs)