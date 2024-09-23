from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import get_month_date_range

from ..serializers import CardPaymentSerializer
from ..models import CardPayment
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CardPaymentApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            card_payments = CardPayment.objects.filter(user=request.user)
            serializer = CardPaymentSerializer(card_payments, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = CardPaymentSerializer(data=request.data) 
        if serializer.is_valid():
            expense = serializer.save(user=request.user)
            return Response({"data": CardPaymentSerializer(expense).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            card_payment = CardPayment.objects.get(pk=pk, user=request.user)
            card_payment.delete()
            return Response({"message": "Card Payment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except CardPayment.DoesNotExist:
            return Response({"error": "Card Payment not found"}, status=status.HTTP_404_NOT_FOUND)