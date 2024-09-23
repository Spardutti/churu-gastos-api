from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import CreditCardSerializer
from ..models import CreditCard
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CreditCardApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk is not None:
            try:
                credit_card = CreditCard.objects.get(pk=pk, user=request.user)
                serializer = CreditCardSerializer(credit_card)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except CreditCard.DoesNotExist:
                return Response({"error": "Credit card not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            try:
                credit_cards = CreditCard.objects.filter(user=request.user)
                serializer = CreditCardSerializer(credit_cards, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        serializer = CreditCardSerializer(data=request.data) 
        if serializer.is_valid():
            expense = serializer.save(user=request.user)
            return Response({"data": CreditCardSerializer(expense).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)