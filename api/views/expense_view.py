from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import ExpenseSerializer
from ..models import Expense
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ExpenseApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)

        if year and month:
            try:
                start_date = datetime(int(year), int(month), 1)
                # Handle last day of the month
                next_month = start_date.replace(day=28) + timedelta(days=4)
                end_date = next_month - timedelta(days=next_month.day)
                
                expenses = Expense.objects.filter(
                    user=request.user,
                    date__range=[start_date, end_date]
                )
            except ValueError:
                    return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            expenses = Expense.objects.filter(user=request.user)

        serializer = ExpenseSerializer(expenses, many=True)
        return Response({"expenses": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data) 
        if serializer.is_valid():
            expense = serializer.save(user=request.user)
            return Response({"expense": ExpenseSerializer(expense).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)