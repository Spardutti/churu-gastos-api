from rest_framework import serializers
from ..models import AccountBudget, Account
from .account_serializer import AccountSerializer   

class AccountBudgetSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), write_only=True, source='account'
    )

    class Meta:
        model = AccountBudget
        fields = ('id', 'account', 'account_id', 'date', 'amount')
