from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import get_month_date_range
from ..serializers import AccountBudgetSerializer
from ..models import AccountBudget
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


class AccountBudgetAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            account_id = request.query_params.get('account_id')
            year = request.query_params.get('year')
            month = request.query_params.get('month')

            if account_id is not None and year and month:
                # Filter by account_id instead of pk
                start_date, end_date = get_month_date_range(year, month)
                try:
                    account_budget = AccountBudget.objects.get(account_id=account_id, user=request.user, date__gte=start_date, date__lte=end_date)
                
                    serializer = AccountBudgetSerializer(account_budget)
                    return Response({"data": serializer.data}, status=status.HTTP_200_OK)
                except:
                    return Response({"error": "No account budgets found for this account"}, status=status.HTTP_404_NOT_FOUND)
                

            
            
            elif year is None or month is None:
                return Response({"error": "Year and month must be provided"}, status=status.HTTP_400_BAD_REQUEST)

            accounts = self.filter_by_months(year, month, request.user)
            serializer = AccountBudgetSerializer(accounts, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        serializer = AccountBudgetSerializer(data=request.data)

        account = request.data.get('account_id')
        date =  timezone.now()

        year = date.year
        month = date.month

        # Check if an account budget already exists for the same month/year
        existing_budget = AccountBudget.objects.filter(
            account_id=account,
            date__year=year,
            date__month=month
        )
        print('existing', existing_budget)

        if existing_budget.exists():
            # Return error response to frontend
            return Response({
                'error': f'A budget for this account already exists for {date.strftime("%B %Y")}.'
            }, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        account_budget = AccountBudget.objects.get(pk=pk, user=request.user)
        serializer = AccountBudgetSerializer(account_budget, data=request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            account_budget = AccountBudget.objects.get(pk=pk, user=request.user)
            account_budget.delete()
            return Response({"message": "Account Budget deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except AccountBudget.DoesNotExist:
            return Response({"error": "Account Budget not found"}, status=status.HTTP_404_NOT_FOUND)

    def filter_by_months(self, year, month, user):
        start_date, end_date = get_month_date_range(year, month)
        return AccountBudget.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')