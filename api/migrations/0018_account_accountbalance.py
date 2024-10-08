# Generated by Django 5.1.1 on 2024-10-06 15:31

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_expense_is_recursive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccountBalance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='api.account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_balances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
