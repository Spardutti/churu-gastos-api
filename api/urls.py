from django.urls import path
from .views import CategoryApiView, ExpenseApiView, BudgetApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView

urlpatterns = [
    path('categories/', CategoryApiView.as_view(), name='Category'),
    path('categories/<int:pk>/', CategoryApiView.as_view(), name='Category'),
    path('expenses/', ExpenseApiView.as_view(), name='Expense'),
    path('budget/', BudgetApiView.as_view(), name='Budget'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]
