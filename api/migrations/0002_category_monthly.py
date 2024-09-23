# Generated by Django 5.1.1 on 2024-09-21 12:45
from django.db import migrations, models
from datetime import date

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='budget',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='month',
            field=models.DateField(default=date.today().replace(day=1)),
        )
         
    ]