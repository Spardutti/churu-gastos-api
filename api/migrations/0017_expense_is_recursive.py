# Generated by Django 5.1.1 on 2024-09-30 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_normaluser_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='is_recursive',
            field=models.BooleanField(default=False),
        ),
    ]
