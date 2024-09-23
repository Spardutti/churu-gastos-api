from django.urls import path
from .views import CategoryApiView, ExpenseApiView, UserView, UniqueExpenseApiView, CreditCardApiView, CardPaymentApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserView

urlpatterns = [
    path('categories/', CategoryApiView.as_view(), name='Category'),
    path('categories/<int:pk>/', CategoryApiView.as_view(), name='Category'),
    path('expenses/', ExpenseApiView.as_view(), name='Expense'),
    path('unique-expenses/', UniqueExpenseApiView.as_view(), name='UniqueExpense'),
    path('credit-cards/', CreditCardApiView.as_view(), name='CreditCard'),
    path('credit-cards/<int:pk>/', CreditCardApiView.as_view(), name='CreditCard'),
    path('card-payments/', CardPaymentApiView.as_view(), name='CardPayment'),
    path('card-payments/<int:pk>/', CardPaymentApiView.as_view(), name='CardPayment'),
    path('user/', UserView.as_view(), name='User'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserView.as_view(), name='register'),
]
