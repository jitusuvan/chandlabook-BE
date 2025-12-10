# views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .model import Guest
from .serializer import GuestSerializer

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all().order_by('-id')
    serializer_class = GuestSerializer

    # Search + Filter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city']          # for exact filtering ?city=Pune
    search_fields = ['first_name', 'last_name', 'surname', 'city', 'mobile_no']  # ?search=raj
