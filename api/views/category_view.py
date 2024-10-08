from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import get_month_date_range
from ..serializers import CategorySerializer
from ..models import Category
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

class CategoryApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        # Show single category
        if pk is not None:
            try:
                category = Category.objects.get(pk=pk, user=request.user)
                serializer = CategorySerializer(category)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        # List categories by year and month
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if year is None or month is None:
            return Response({"error": "Year and month must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        categories = self.filter_categories(request.user, year=int(year), month=int(month))
        
        # Check if categories exist for any month in the past
        past_categories_exist = self.past_categories_exist(request, year=int(year), month=int(month))

        # is_new_month is True only if past categories exist but no categories for the given month and year
        is_new_month = past_categories_exist and not categories.exists()

        # Calculate the total budget for the filtered categories
        total_budget = categories.aggregate(total=Sum('budget'))['total'] or 0

        serializer = CategorySerializer(categories, many=True)
        return Response({"data": serializer.data, "monthly_budget": total_budget, "is_new_month": is_new_month}, status=status.HTTP_200_OK)

    def post(self, request):
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid():
            category_serializer.save(user=request.user)
            return Response({"data": category_serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk, user=request.user)
            category_serializer = CategorySerializer(category, data=request.data, partial=True)
            if category_serializer.is_valid():
                category_serializer.save()
                return Response({"data": category_serializer.data}, status=status.HTTP_200_OK)
            return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk, user=request.user)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    def filter_categories(self, user, year, month):
        """
        Filter categories by date range.
        """
        start_date, end_date = get_month_date_range(year, month)
        return Category.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')

    
    def past_categories_exist(self, request, year, month):
        start_date, end_date = get_month_date_range(year=year, month=month)
        return Category.objects.filter(
            user=request.user
        ).exclude(
            date=start_date
        ).exists()
