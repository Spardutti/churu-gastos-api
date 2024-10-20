from rest_framework import serializers
from ..models import UniqueExpense, AccountBudget
from .account_budget_serializer import AccountBudgetSerializer

class UniqueExpenseSerializer(serializers.ModelSerializer):

    
    account_budget_id = serializers.PrimaryKeyRelatedField(
        queryset=AccountBudget.objects.all(), write_only=True, source='account_budget'
    )

    class Meta:
        model = UniqueExpense
        fields = ('id', 'date', 'description', 'amount', 'account_budget_id')