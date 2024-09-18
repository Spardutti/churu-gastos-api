from django.db import models

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)
    description = models.TextField(blank=True, null=True, max_length=100)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)