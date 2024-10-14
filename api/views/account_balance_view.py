from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import get_month_date_range
from ..serializers import AccountBudgetSerializer
from ..models import AccountBudget
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

class AccountBalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            if year is None or month is None:
                return Response({"error": "Year and month must be provided"}, status=status.HTTP_400_BAD_REQUEST)

            accounts = self.filter_by_months(year, month, request.user)
            serializer = AccountBudgetSerializer(accounts, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        serializer = AccountBudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        account_balance = AccountBudget.objects.get(pk=pk, user=request.user)
        serializer = AccountBudgetSerializer(account_balance, data=request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            account_balance = AccountBudget.objects.get(pk=pk, user=request.user)
            account_balance.delete()
            return Response({"message": "Account Balance deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except AccountBudget.DoesNotExist:
            return Response({"error": "Account Balance not found"}, status=status.HTTP_404_NOT_FOUND)

    def filter_by_months(self, year, month, user):
        start_date, end_date = get_month_date_range(year, month)
        return AccountBudget.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')