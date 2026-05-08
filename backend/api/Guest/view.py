# views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .model import Guest
from .serializer import GuestSerializer


class GuestViewSet(viewsets.ModelViewSet):
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city']
    search_fields = ['first_name', 'last_name', 'surname', 'city', 'mobile_no']
    
    def get_queryset(self):
        return Guest.objects.filter(user=self.request.user).order_by('-id')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
  # NEW API
    @action(detail=False, methods=['get'])
    def cities(self, request):

        cities = (
            Guest.objects
            .filter(user=request.user)
            .exclude(city__isnull=True)
            .exclude(city__exact='')
            .values_list('city', flat=True)
            .distinct()
            .order_by('city')
        )

        return Response(cities)