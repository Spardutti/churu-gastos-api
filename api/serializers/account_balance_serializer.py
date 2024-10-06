from rest_framework import serializers
from ..models import AccountBalance, Account
from .account_serializer import AccountSerializer   

class AccountBalanceSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), write_only=True, source='account'
    )

    class Meta:
        model = AccountBalance
        fields = ('id', 'account', 'account_id', 'date', 'balance')
