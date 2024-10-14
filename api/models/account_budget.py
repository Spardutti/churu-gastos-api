from django.db import models
from django.utils import timezone

from api.utils import set_timezone_aware_dates

class AccountBudget(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='budget')
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE, related_name='account_budget')

    def save(self, *args, **kwargs):
        set_timezone_aware_dates(self, self.user, 'date')

        super(AccountBudget, self).save(*args, **kwargs)