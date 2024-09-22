from django.db import migrations

def transfer_budget_to_category(apps, schema_editor):
    Budget = apps.get_model('api', 'Budget')
    Category = apps.get_model('api', 'Category')

    # Assuming there's a relationship between Budget and Category
    for budget in Budget.objects.all():
        # Assuming each budget relates to a category and user
        category = Category.objects.get(id=budget.category_id.id)
        category.budget = budget.amount  # Assign budget amount to category
        category.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_category_monthly'),  # Replace with the actual migration you generated
    ]

    operations = [
        migrations.RunPython(transfer_budget_to_category),
    ]
