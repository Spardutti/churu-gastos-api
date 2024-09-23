from rest_framework import serializers
from ..models import CreditCard


class CreditCardSerializer(serializers.ModelSerializer):
    card_last_4 = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model=CreditCard
        fields = ('id', 'name', 'card_last_4', 'card_type')
