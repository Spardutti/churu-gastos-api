from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import get_month_date_range

from ..serializers import ExpenseSerializer
from ..models import Expense
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ExpenseApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)
        category_id = request.query_params.get('category_id', None)

        try:
            expenses = self.get_filtered_expenses(request.user, year, month, category_id)
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ExpenseSerializer(expenses, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data) 
        if serializer.is_valid():
            expense = serializer.save(user=request.user)
            return Response({"data": ExpenseSerializer(expense).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            expense = Expense.objects.get(pk=pk, user=request.user)
            expense.delete()
            return Response({"message": "Expense deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Expense.DoesNotExist:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, pk=None):
        try:
            expense = Expense.objects.get(pk=pk, user=request.user)
            serializer = ExpenseSerializer(expense, data=request.data, partial=True)
            if serializer.is_valid():
                expense = serializer.save()
                return Response({"data": ExpenseSerializer(expense).data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Expense.DoesNotExist:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def filter_by_user(self, user):
        """
        Returns all expenses for a user.
        """
        return Expense.objects.filter(user=user)
    
    def filter_by_date_and_category(self, user, start_date, end_date, category_id=None):
        """
        Filter expenses by date and category if provided.
        """
        filter_args = {
            'user': user,
            'date__gte': start_date,
            'date__lt': end_date
        }

        if category_id:
            filter_args['category_id'] = category_id

        return Expense.objects.filter(**filter_args)
    
    def get_filtered_expenses(self, user, year, month, category_id):
        """
        Filter expenses by year, month, and category if provided.
        """
        if year and month:
            start_date, end_date = get_month_date_range(year, month)
            return self.filter_by_date_and_category(user, start_date, end_date, category_id)
        return self.filter_by_user(user)