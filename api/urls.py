from django.urls import path
from .views import get_categories, create_category

urlpatterns = [
    path('categories/', get_categories),
    path('categories/create/', create_category)
]
