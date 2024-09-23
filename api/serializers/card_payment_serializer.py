from rest_framework import serializers
from ..models import CardPayment


class CardPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model=CardPayment
        fields = ('id', 'card_id', 'description', 'total_amount', 'number_of_payments', 'initial_payment_date', 'monthly_payment_amount', 'payments_made', 'end_payment_date', 'next_payment_date')
        read_only_fields = ('monthly_payment_amount', 'end_payment_date')