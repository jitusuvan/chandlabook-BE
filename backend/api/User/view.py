from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from api.User.serializers import UserSerializer
from api.UserProfile.model import UserProfile
from api.UserProfile.serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class GetMyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


