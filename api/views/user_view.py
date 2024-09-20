from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import NormalUser


class UserView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            # Protect the GET request - user must be authenticated
            return [IsAuthenticated()]
        
        elif self.request.method == 'POST':
            # Allow the POST request for anyone (public access)
            return [AllowAny()]
        
        return super().get_permissions()
    
    def get(self, request):
        try:
            user = NormalUser.objects.get(pk=request.user.id)
        except ValueError:
            return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)