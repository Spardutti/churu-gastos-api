from rest_framework import serializers
from ..models import Credit


class CreditSerializer(serializers.ModelSerializer):

    class Meta:
        model=Credit
        fields = ('id', 'description', 'number_of_payments', 'monthly_payment_amount', 'payments_made', 'next_payment_date', 'is_active', 'created_at')
        read_only_fields = ('end_payment_date',)