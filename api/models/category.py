from django.db import models
from datetime import date

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE, related_name='categories')

    # Track the month using a DateField, defaulting to the first day of the current month
    month = models.DateField(default=date.today().replace(day=1))

    budget = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name