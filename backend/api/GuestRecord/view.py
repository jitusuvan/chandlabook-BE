# views.py
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Q
from datetime import date
from .model import GuestRecord
from .serializer import GuestRecordSerializer

class GuestRecordViewSet(viewsets.ModelViewSet):
    serializer_class = GuestRecordSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['guest', 'event', 'select', 'pay_later']
    search_fields = ['guest__first_name', 'guest__surname', 'event', 'select']
    
    def get_queryset(self):
        return GuestRecord.objects.filter(guest__user=self.request.user).order_by('-date')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        
        aavel_total = queryset.filter(select='aavel').aggregate(Sum('amount'))['amount__sum'] or 0
        mukel_total = queryset.filter(select='mukel').aggregate(Sum('amount'))['amount__sum'] or 0
        difference = aavel_total - mukel_total
        
        totals = {
            'aavel_total': aavel_total,
            'mukel_total': mukel_total,
            'difference': difference
        }
        response.data['results'] = [totals] + response.data['results']
        
        return response

    @action(detail=False, methods=['get'])
    def today(self, request):
        today_date = date.today()
        queryset = self.get_queryset().filter(date=today_date)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        today_date = date.today()
        queryset = self.get_queryset().filter(date__gt=today_date).order_by('date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
