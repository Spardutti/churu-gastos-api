from datetime import date, timedelta
from multiprocessing import Value
from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import get_month_date_range
from ..serializers import CategorySerializer
from ..models import Category
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

class NewMonthApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self.get_past_month_categories(request)


    def get_past_month_categories(self, request):
        start_date_of_previous_month, last_day_of_previous_month = self.get_previous_month_date_range()

        categories = Category.objects.filter(user=request.user, date__gte=start_date_of_previous_month, date__lt=last_day_of_previous_month)
        try:
            self.create_categories_for_new_month(categories)
            return Response({"message": "Categories created successfully"}, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

    def get_previous_month_date_range(self):
        today = date.today()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        start_date = last_day_of_previous_month.replace(day=1)
        start_date_of_previous_month = start_date
        return start_date_of_previous_month, last_day_of_previous_month
    
    def create_categories_for_new_month(self, categories):
        for category in categories:
            Category.objects.create(budget=category.budget, name=category.name, user=category.user)
            