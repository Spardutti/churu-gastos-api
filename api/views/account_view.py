
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import AccountSerializer
from ..models import Account
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class AccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AccountSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        account = Account.objects.get(pk=pk, user=request.user)
        serializer = AccountSerializer(account, data=request.data, context={'request': request}, partial=True)  # Enable partial update
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            account = Account.objects.get(pk=pk, user=request.user)
            account.delete()
            return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
