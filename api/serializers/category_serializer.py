from datetime import datetime, timedelta
from rest_framework import serializers

from api.serializers.budget_serializer import BudgetSerializer
from api.utils import get_month_date_range
from ..models import Category, Budget


class CategorySerializer(serializers.ModelSerializer):

    current_month_budget = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('id', 'name', 'current_month_budget', 'created_at', 'updated_at')
    
    def get_current_month_budget(self, obj):
        # Calculate start and end dates for the current month
        now = datetime.now()
        start_date, end_date = get_month_date_range(year=now.year, month=now.month)

        try:
            budget = Budget.objects.get(category_id=obj.id, date__gte=start_date, date__lt=end_date)
            return BudgetSerializer(budget).data
        except Budget.DoesNotExist:
            return None