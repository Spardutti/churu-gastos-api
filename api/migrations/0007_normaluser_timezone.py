# Generated by Django 5.1.1 on 2024-09-22 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_uniqueexpense_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='normaluser',
            name='timezone',
            field=models.CharField(default='America/Argentina/Buenos_Aires', max_length=63),
            preserve_default=False,
        ),
    ]