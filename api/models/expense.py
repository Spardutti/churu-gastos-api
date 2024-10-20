from django.utils import timezone
from django.db import models

from api.utils import set_timezone_aware_dates

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True, max_length=100)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE)
    account_budget = models.ForeignKey('AccountBudget', on_delete=models.CASCADE)

    is_recursive = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        set_timezone_aware_dates(self, self.user, 'date')

        super(Expense, self).save(*args, **kwargs)