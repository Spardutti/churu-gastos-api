# Generated by Django 5.1.1 on 2024-10-20 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_expense_account_id_uniqueexpense_account_id'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='accountbudget',
            name='unique_account_budget_per_month',
        ),
    ]
