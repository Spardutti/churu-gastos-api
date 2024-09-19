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

        if year and month:
            try:
                start_date, end_date = get_month_date_range(year=year, month=month)

                filter_args = {
                'user': request.user,
                'date__gte': start_date,
                'date__lt': end_date
                }

                if category_id:
                    filter_args['category_id'] = category_id
                    
                expenses = Expense.objects.filter(**filter_args)
            except ValueError:
                    return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST) 
            
        else:
            expenses = Expense.objects.filter(user=request.user)

        serializer = ExpenseSerializer(expenses, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data) 
        if serializer.is_valid():
            expense = serializer.save(user=request.user)
            return Response({"data": ExpenseSerializer(expense).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)