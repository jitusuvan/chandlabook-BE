# views.py
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Q
from .model import GuestRecord
from .serializer import GuestRecordSerializer

class GuestRecordViewSet(viewsets.ModelViewSet):
    queryset = GuestRecord.objects.all().order_by('-date')
    serializer_class = GuestRecordSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['guest', 'event', 'select', 'pay_later']    # ?event=marriage
    search_fields = ['guest__first_name', 'guest__surname', 'event', 'select']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        
        aavel_total = queryset.filter(select='aavel').aggregate(Sum('amount'))['amount__sum'] or 0
        mukel_total = queryset.filter(select='mukel').aggregate(Sum('amount'))['amount__sum'] or 0
        difference = aavel_total - mukel_total
        
        # Add totals to results
        totals = {
            'aavel_total': aavel_total,
            'mukel_total': mukel_total,
            'difference': difference
        }
        response.data['results'] = [totals] + response.data['results']
        
        return response
