from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import CategorySerializer
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
        
                return Response({"category": serializer.data}, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # List
        else:
            categories = Category.objects.filter(user=request.user).values('id', 'name', 'budget')
            serializer = CategorySerializer(categories, many=True)
        
            return Response({"categories": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data) 
        if serializer.is_valid():
            category = serializer.save(user=request.user)
            return Response({"category": CategorySerializer(category).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)