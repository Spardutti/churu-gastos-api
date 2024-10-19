from os import write
from rest_framework import serializers
from ..models import Expense, AccountBudget
from .account_budget_serializer import AccountBudgetSerializer


class ExpenseSerializer(serializers.ModelSerializer):
     
    
    # Primary key related field for account_budget_id (used for writing)
    account_budget_id = serializers.PrimaryKeyRelatedField(
        queryset=AccountBudget.objects.all(), write_only=True, source='account_budget'
    )

    class Meta:
        model = Expense
        fields = (
            'id', 'date', 'description', 'amount', 'category_id', 'account_budget_id', 'is_recursive',
            'created_at', 'updated_at'
        )
