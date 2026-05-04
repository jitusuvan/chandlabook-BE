from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from api.UserProfile.model import UserProfile
from api.UserProfile.serializers import UserProfileSerializer

class GetMyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get or create profile for current user
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

