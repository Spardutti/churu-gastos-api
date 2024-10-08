from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import get_month_date_range

from ..serializers import CreditSerializer
from ..models import Credit
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import models

class CreditApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            credit = Credit.objects.filter(user=request.user)
            serializer = CreditSerializer(credit, many=True)
            total = self.calculate_current_month_total(request)
            return Response({"data": serializer.data, "month_total": total}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = CreditSerializer(data=request.data) 
        if serializer.is_valid():
            credit = serializer.save(user=request.user)
            return Response({"data": CreditSerializer(credit).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            credit = Credit.objects.get(pk=pk, user=request.user)
            credit.delete()
            return Response({"message": "Card Payment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Credit.DoesNotExist:
            return Response({"error": "Card Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, pk=None):
        try:
            credit = Credit.objects.get(pk=pk, user=request.user)
            serializer = CreditSerializer(credit, data=request.data, partial=True)
            if serializer.is_valid():
                credit = serializer.save()
                return Response({"data": CreditSerializer(credit).data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Credit.DoesNotExist:
            return Response({"error": "Card Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def calculate_current_month_total(self, request):
        now = datetime.now()
        month_start, month_end = get_month_date_range(month=now.month, year=now.year)

        return Credit.objects.filter(
            user=request.user,
            next_payment_date__gte=month_start,
            next_payment_date__lte=month_end
        ).aggregate(total=models.Sum('monthly_payment_amount'))['total'] or 0