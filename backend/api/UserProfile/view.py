from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .model import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.all()
    
    def get_object(self):
        return UserProfile.objects.get_or_create(user_id=self.kwargs['pk'])[0]
