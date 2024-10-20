import django.db.models.deletion
from django.db import migrations, models


def assign_default_account_budget(apps, schema_editor):
    AccountBudget = apps.get_model('api', 'AccountBudget')
    Expense = apps.get_model('api', 'Expense')
    UniqueExpense = apps.get_model('api', 'UniqueExpense')

    # Get or create the first account budget
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
        # Step 1: Add the field with null=True
        migrations.AddField(
            model_name='expense',
            name='account_budget',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.AccountBudget'),
        ),
        migrations.AddField(
            model_name='uniqueexpense',
            name='account_budget',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.AccountBudget'),
        ),
        # Step 2: Run Python function to assign default account budgets
        migrations.RunPython(assign_default_account_budget),
        # Step 3: Alter the field to make it non-nullable
        migrations.AlterField(
            model_name='expense',
            name='account_budget',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, to='api.AccountBudget'),
        ),
        migrations.AlterField(
            model_name='uniqueexpense',
            name='account_budget',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, to='api.AccountBudget'),
        ),
    ]
