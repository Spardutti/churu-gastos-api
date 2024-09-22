from rest_framework import serializers
from ..models import UniqueExpense

class UniqueExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UniqueExpense
        fields = ('id', 'date', 'name', 'amount')