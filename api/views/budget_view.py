from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import get_month_date_range

from ..serializers import BudgetSerializer
from ..models import Budget
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta

class BudgetApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk is not None:
            try:
                budget = Budget.objects.get(pk=pk, user=request.user)
                serializer = BudgetSerializer(budget)
                return Response({"budget": serializer.data}, status=status.HTTP_200_OK)
            except Budget.DoesNotExist:
                return Response({"error": "Budget not found"}, status=status.HTTP_404_NOT_FOUND)
            
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)
        category_id = request.query_params.get('category_id', None)

        if year and month and category_id:
            try:
                start_date, end_date = get_month_date_range(year=year, month=month)
                budgets = Budget.objects.filter(user=request.user, date__gte=start_date, date__lt=end_date, category_id=category_id)
                serializer = BudgetSerializer(budgets, many=True)
                
                return Response({"budgets": serializer.data}, status=status.HTTP_200_OK)
            except ValueError:
                return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Year, month and category_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        serializer = BudgetSerializer(data=request.data) 
        if serializer.is_valid():
            budget = serializer.save(user=request.user)
            return Response({"budget": BudgetSerializer(budget).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)