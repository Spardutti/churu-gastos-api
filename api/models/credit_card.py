from django.db import models

from api.utils import set_timezone_aware_dates

class CreditCard(models.Model):
    name = models.CharField(max_length=100)
    card_last_4 = models.CharField(max_length=4, null=True, blank=True)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE)
    card_type = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        set_timezone_aware_dates(self, self.user)

        super(CreditCard, self).save(*args, **kwargs)