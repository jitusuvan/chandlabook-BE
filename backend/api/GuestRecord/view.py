# views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .model import GuestRecord
from .serializer import GuestRecordSerializer

class GuestRecordViewSet(viewsets.ModelViewSet):
    queryset = GuestRecord.objects.all().order_by('-date')
    serializer_class = GuestRecordSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['guest', 'event', 'select']    # ?event=marriage
    search_fields = ['guest__first_name', 'guest__surname', 'event', 'select']
