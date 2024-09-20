from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import CategorySerializer, BudgetSerializer
from ..models import Category
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CategoryApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        # Show
        if pk is not None:
            try:
                category = Category.objects.get(pk=pk, user=request.user)
                serializer = CategorySerializer(category)
        
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # List
        else:
            categories = Category.objects.filter(user=request.user)
            serializer = CategorySerializer(categories, many=True)
        
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid():
            category = category_serializer.save(user=request.user)
            
            # Create an expense related to the category
            budget_data = {
                "amount": request.data.get("amount"),
                "category_id": category.id,
                "user": request.user.id,
                "date": request.data.get("date", datetime.now().date())
            }
            
            # Validate and save the expense
            budget_serializer = BudgetSerializer(data=budget_data)
            if budget_serializer.is_valid():
                budget_serializer.save(user=request.user, category_id=category)

                return Response(
                    {
                        "data": category_serializer.data,
                    }, 
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(budget_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)