from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import get_month_date_range
from ..models import AccountBudget, Expense, UniqueExpense
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CurrentMonthAccountBudgetAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if year is None and month is None:
            return Response({"error": "Year and month must be provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        budget = self.budget(year, month)

        return Response({"data": { "accounts_budget": budget}
        }, status=status.HTTP_200_OK)


    def total_accounts_budget(self, account_budgets):
        total = 0
        for budget in account_budgets:
            total += budget.amount
        return total
    
    def total_expenses(self, expenses):
        total = 0
        for expense in expenses:
            total += expense.amount
        return total
    
    def total_unique_expenses(self, unique_expenses):
        total = 0
        for unique_expense in unique_expenses:
            total += unique_expense.amount
        return total
    
    def budget(self, year, month):
        start_date, end_date = get_month_date_range(year, month)

        total_account_budgets = self.total_accounts_budget(AccountBudget.objects.filter(user=self.request.user, date__lte=end_date, date__gte=start_date))
        total_expenses = self.total_expenses(Expense.objects.filter(user=self.request.user, date__lte=end_date, date__gte=start_date))
        total_unique_expenses = self.total_unique_expenses(UniqueExpense.objects.filter(user=self.request.user, date__lte=end_date, date__gte=start_date))
        return total_account_budgets - total_expenses - total_unique_expenses