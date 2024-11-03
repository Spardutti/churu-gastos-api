from rest_framework import serializers
from ..models import AccountBudget, Account, Expense
from .account_serializer import AccountSerializer
from django.db.models import Sum


class AccountBudgetSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), write_only=True, source='account'
    )

    remaining_balance = serializers.SerializerMethodField()

    class Meta:
        model = AccountBudget
        fields = ('id', 'account', 'account_id', 'date', 'budget', 'remaining_balance')


    def get_remaining_balance(self, obj):
        # Calculate total expenses associated with this AccountBudget
        total_expenses = Expense.objects.filter(account_budget=obj).aggregate(
            total=Sum('amount')
        )['total'] or 0  # Defaults to 0 if no expenses are found

        # Calculate remaining budget
        remaining_balance = obj.budget - total_expenses
        return remaining_balance