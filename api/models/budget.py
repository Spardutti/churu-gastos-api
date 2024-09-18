from django.db import models

class Budget(models.Model):
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey('NormalUser', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)