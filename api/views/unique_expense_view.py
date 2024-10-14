from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import get_month_date_range

from ..serializers import UniqueExpenseSerializer
from ..models import UniqueExpense
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class UniqueExpenseApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)

        if year and month:
            unique_expenses = self.filter_unique_expense(request.user, year, month)
            serializer = UniqueExpenseSerializer(unique_expenses, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"error": "Year and month must be provided"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = UniqueExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            unique_expense = UniqueExpense.objects.get(pk=pk, user=request.user)
            unique_expense.delete()
            return Response({"message": "Unique Expense deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except UniqueExpense.DoesNotExist:
            return Response({"error": "Unique Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, pk=None):
        try:
            unique_expense = UniqueExpense.objects.get(pk=pk, user=request.user)
            serializer = UniqueExpenseSerializer(unique_expense, data=request.data, partial=True)
            if serializer.is_valid():
                unique_expense = serializer.save()
                return Response({"data": UniqueExpenseSerializer(unique_expense).data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UniqueExpense.DoesNotExist:
            return Response({"error": "Unique Expense not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def filter_unique_expense(self, user, year, month):
        start_date, end_date = get_month_date_range(year=year, month=month)
        return self.unique_expenses_by_month(user=user, start_date=start_date, end_date=end_date)
    
    def unique_expenses_by_month(self, user, start_date, end_date):
        """
        Returns all unique expenses for a user filtered by the month.
        """
        return UniqueExpense.objects.filter(user=user, date__gte=start_date, date__lt=end_date)