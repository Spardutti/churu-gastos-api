from django.db import models
from django.utils import timezone

from api.utils import set_timezone_aware_dates

class AccountBalance(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='balances')
    date = models.DateTimeField(default=timezone.now)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE, related_name='account_balances')

    def save(self, *args, **kwargs):
        set_timezone_aware_dates(self, self.user, 'date')

        super(AccountBalance, self).save(*args, **kwargs)