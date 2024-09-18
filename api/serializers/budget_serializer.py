from rest_framework import serializers
from ..models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('id', 'amount', 'date', 'category_id', 'created_at', 'updated_at')