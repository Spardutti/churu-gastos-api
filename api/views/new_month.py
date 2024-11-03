from datetime import date, timedelta
from django.utils import timezone
from dateutil import parser
from django.utils import timezone

from hmac import new
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Category, Expense, AccountBudget
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class NewMonthApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self.get_past_month_categories(request)

    def get_past_month_categories(self, request):
        raw_date = request.data.get('date')   
        if raw_date:
            try:
                parsed_date = parser.parse(raw_date)
            except (ValueError, TypeError) as e:
                print(f"Invalid date format: {e}")
                return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            parsed_date = timezone.now()
        start_date_of_previous_month, last_day_of_previous_month = self.get_previous_month_date_range()

        categories = Category.objects.filter(user=request.user, date__gte=start_date_of_previous_month, date__lt=last_day_of_previous_month)
        expenses = Expense.objects.filter(user=request.user, date__gte=start_date_of_previous_month, date__lt=last_day_of_previous_month, is_recursive=True)
        account_budgets = AccountBudget.objects.filter(user=request.user, date__gte=start_date_of_previous_month, date__lt=last_day_of_previous_month)

        try:
            # Create categories and map old IDs to new ones
            old_to_new_category_mapping = self.create_categories_for_new_month(categories, parsed_date)

            # Create new account budgets and get old-to-new budget mapping
            old_to_new_account_budget_mapping = self.create_account_budgets_for_new_month(account_budgets, parsed_date)
           
            # Create recursive expenses using the new category IDs
            self.create_recursive_expenses(expenses, old_to_new_account_budget_mapping, old_to_new_category_mapping, parsed_date)
            return Response({"message": "Categories and expenses created successfully"}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            print(f"Error: {e}")

            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

    def get_previous_month_date_range(self):
        today = date.today()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        start_date_of_previous_month = last_day_of_previous_month.replace(day=1)
        return start_date_of_previous_month, last_day_of_previous_month
    
    def create_account_budgets_for_new_month(self, accounts, parsed_date):
        old_to_new_account_budget_mapping = {}
        for account in accounts:
            # Create new account budget for the new month
            new_budget = AccountBudget.objects.create(
                account=account.account,
                budget=account.budget,
                user=account.user,
                date=parsed_date
            )
            # Map old account budget ID to new account budget instance
            old_to_new_account_budget_mapping[account.id] = new_budget
        return old_to_new_account_budget_mapping

    
    def create_categories_for_new_month(self, categories, parsed_date):
        old_to_new_category_mapping = {}
        for category in categories:
            new_category = Category.objects.create(budget=category.budget, name=category.name, user=category.user, date=parsed_date)
            old_to_new_category_mapping[category.id] = new_category
        return old_to_new_category_mapping

    def create_recursive_expenses(self, expenses, old_to_new_account_budget_mapping, old_to_new_category_mapping, parsed_date):
        for expense in expenses:
            new_category = old_to_new_category_mapping.get(expense.category_id.id)
            new_account_budget = old_to_new_account_budget_mapping.get(expense.account_budget.id)


            if new_category is None or new_account_budget is None:
                continue   
            Expense.objects.create(
                amount=expense.amount,
                category_id=new_category,  # Use the new category ID
                description=expense.description,
                is_recursive=expense.is_recursive,
                user=expense.user,
                date=parsed_date,
                account_budget=new_account_budget
            )
