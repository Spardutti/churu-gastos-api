from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

from api.utils import get_month_date_range

from ..serializers import BudgetSerializer
from ..models import Budget
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class BudgetApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        if pk is not None:
            try:
                budget = self.get_budget_by_pk(pk)
            except Budget.DoesNotExist:
                return Response({"error": "Budget not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = BudgetSerializer(budget)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)
        category_id = request.query_params.get('category_id', None)

        try:
            budgets = self.get_filtered_budgets(request.user, year, month, category_id)
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BudgetSerializer(budgets, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BudgetSerializer(data=request.data) 
        if serializer.is_valid():
            budget = serializer.save(user=request.user)
            return Response({"data": BudgetSerializer(budget).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_budget_by_pk(self, pk):
        try:
            return Budget.objects.get(pk=pk)
        except Budget.DoesNotExist:
            return None
    
    def filter_by_user(self, user):
        """
        Returns all budgets for a user.
        """
        return Budget.objects.filter(user=user)
    
    def filter_by_date_and_category(self, user, start_date, end_date, category_id=None):
        """
        Filter budgets by date and category if provided.
        """
        filter_args = {
            'user': user,
            'date__gte': start_date,
            'date__lt': end_date
        }

        if category_id:
            filter_args['category_id'] = category_id

        return self.filter_by_user(user).filter(**filter_args)
    
    def get_filtered_budgets(self, user, year, month, category_id):
        """
        Filter budgets by year, month, and category if provided.
        """
        if year and month:
            start_date, end_date = get_month_date_range(year, month)
            return self.filter_by_date_and_category(user, start_date, end_date, category_id)
        return self.filter_by_user(user)