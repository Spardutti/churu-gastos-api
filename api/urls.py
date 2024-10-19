from django.urls import path
from .views import CategoryApiView, ExpenseApiView, UserView, UniqueExpenseApiView, CreditApiView, NewMonthApiView, AccountAPIView, AccountBudgetAPIView, CurrentMonthAccountBudgetAPIView, AccountBudgetExpensesAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserView

urlpatterns = [
    path('categories/', CategoryApiView.as_view(), name='Category'),
    path('categories/<int:pk>/', CategoryApiView.as_view(), name='Category'),
    path('new-month/', NewMonthApiView.as_view(), name='NewMonth'),
    path('expenses/', ExpenseApiView.as_view(), name='Expense'),
    path('expenses/<int:pk>/', ExpenseApiView.as_view(), name='Expense'),
    path('unique-expenses/', UniqueExpenseApiView.as_view(), name='UniqueExpense'),
    path('unique-expenses/<int:pk>/', UniqueExpenseApiView.as_view(), name='UniqueExpense'),
    path('credits/', CreditApiView.as_view(), name='CardPayment'),
    path('credits/<int:pk>/', CreditApiView.as_view(), name='CardPayment'),
    path('accounts/', AccountAPIView.as_view(), name='Account'),
    path('accounts/<int:pk>', AccountAPIView.as_view(), name='Account'),
    path('account-budget/', AccountBudgetAPIView.as_view(), name='AccountBalance'),
    path('account-budget/<int:pk>', AccountBudgetAPIView.as_view(), name='AccountBalance'),
    path('monthly-account-budget', CurrentMonthAccountBudgetAPIView.as_view(), name='MonthlyAccountBalance'),
    path('account-budget-expenses', AccountBudgetExpensesAPIView.as_view(), name='AccountBudgetExpenses'),
    path('user/', UserView.as_view(), name='User'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserView.as_view(), name='register'),
]
