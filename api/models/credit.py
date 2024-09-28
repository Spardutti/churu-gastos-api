from datetime import date
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from ..managers import CreditManager

from api.utils import set_timezone_aware_dates

class Credit(models.Model):
    description = models.CharField(max_length=100)
    number_of_payments = models.IntegerField(validators=[MinValueValidator(1)])
    monthly_payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE)
    payments_made = models.IntegerField(default=0)
    next_payment_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_payment_complete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CreditManager()
    
    def save(self, *args, **kwargs):
        set_timezone_aware_dates(self, self.user, 'next_payment_date')

        if not self.pk:
            user_now = timezone.now().astimezone(timezone.get_current_timezone())
            
            # Compare the month and year of next_payment_date with the current date
            if (self.next_payment_date.month != user_now.month or 
                self.next_payment_date.year != user_now.year):
                self.is_active = False
                self.payments_made = 0
            else:
                self.is_active = True
                self.payments_made = 1

        super(Credit, self).save(*args, **kwargs)
