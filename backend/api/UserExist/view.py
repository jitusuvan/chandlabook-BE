# api/UserExist/view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

class UserExistView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {"exists": False, "message": "Email is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_exists = User.objects.filter(email=email).exists()
        return Response({"exists": user_exists}, status=status.HTTP_200_OK)