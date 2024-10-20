import django.db.models.deletion
from django.db import migrations, models


def assign_default_account_budget(apps, schema_editor):
    AccountBudget = apps.get_model('api', 'AccountBudget')
    Expense = apps.get_model('api', 'Expense')
    UniqueExpense = apps.get_model('api', 'UniqueExpense')

    # Get the first account budget or create a default one if none exists
    account_budget = AccountBudget.objects.first()

    if not account_budget:
        account_budget = AccountBudget.objects.create(name='Default Account')

    # Assign the account budget to all existing expenses
    for expense in Expense.objects.all():
        expense.account_budget_id = account_budget.id
        expense.save()

    for unique_expense in UniqueExpense.objects.all():
        unique_expense.account_budget_id = account_budget.id
        unique_expense.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_rename_amount_accountbudget_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='account_budget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AccountBudget'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uniqueexpense',
            name='account_budget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AccountBudget'),
            preserve_default=False,
        ),
        migrations.RunPython(assign_default_account_budget),
    ]
