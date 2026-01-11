from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count
from api.Event.model import Event
from api.Guest.model import Guest
from api.GuestRecord.model import GuestRecord
from api.Expense.model import Expense

class DashboardView(APIView):
    def get(self, request):
        # Total counts
        total_events = Event.objects.count()
        total_guests = Guest.objects.count()
        total_records = GuestRecord.objects.count()
        
        # Total amounts
        total_amount = GuestRecord.objects.aggregate(total=Sum('amount'))['total'] or 0
        aavel_total = GuestRecord.objects.filter(select='aavel').aggregate(total=Sum('amount'))['total'] or 0
        mukel_total = GuestRecord.objects.filter(select='mukel').aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'total_events': total_events,
            'total_guests': total_guests,
            'total_records': total_records,
            'total_amount': total_amount,
            'aavel_total': aavel_total,
            'mukel_total': mukel_total,
            'difference': aavel_total - mukel_total,
            'total_expenses': total_expenses,
            'net_amount': total_amount - total_expenses
        })