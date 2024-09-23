from django.db import models
from django.core.validators import MinValueValidator
from dateutil.relativedelta import relativedelta


from api.utils import set_timezone_aware_dates

class CardPayment(models.Model):
    description = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_payments = models.IntegerField(validators=[MinValueValidator(1)])
    initial_payment_date = models.DateTimeField(null=False)
    monthly_payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE)
    payments_made = models.IntegerField(default=0)
    end_payment_date = models.DateTimeField(null=True, blank=True)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    card_id = models.ForeignKey('CreditCard', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.monthly_payment_amount = self.total_amount / self.number_of_payments

        self.end_payment_date = self.initial_payment_date + relativedelta(months=self.number_of_payments)

        self.end_payment_date = set_timezone_aware_dates(field='end_payment_date', instance=CardPayment, user=self.user)

        if self.payments_made < self.number_of_payments:
            self.next_payment_date = self.initial_payment_date + relativedelta(months=self.payments_made)
            self.next_payment_date = set_timezone_aware_dates(field='next_payment_date', instance=CardPayment, user=self.user)

        super(CardPayment, self).save(*args, **kwargs)

    def make_payment(self):
        if self.payments_made >= self.number_of_payments:
            raise ValueError("All payments have already been made.")
        
        self.payments_made += 1
        self.next_payment_date = self.initial_payment_date + relativedelta(months=self.payments_made)
        self.save()