from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..serializers import ExpenseSerializer, UniqueExpenseSerializer
from ..models import Expense, UniqueExpense

class AccountBudgetExpensesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account_budget_id = request.query_params.get('account_budget_id')
        
        if account_budget_id is None:
            return Response({"error": "account_budget_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            expenses = Expense.objects.filter(account_budget_id=account_budget_id, user=request.user)
            unique_expenses = UniqueExpense.objects.filter(account_budget_id=account_budget_id, user=request.user)

            expense_serializer = ExpenseSerializer(expenses, many=True)
            unique_expense_serializer = UniqueExpenseSerializer(unique_expenses, many=True)

            expenses_with_type = [
                {**expense, "type": "expense"} for expense in expense_serializer.data
            ]
            unique_expenses_with_type = [
                {**unique_expense, "type": "unique_expense"} for unique_expense in unique_expense_serializer.data
            ]

            combined_data = expenses_with_type + unique_expenses_with_type

            return Response({"data": combined_data}, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid account_budget_id"}, status=status.HTTP_400_BAD_REQUEST)
