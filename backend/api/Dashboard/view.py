from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from api.Event.model import Event
from api.Guest.model import Guest
from api.GuestRecord.model import GuestRecord
from api.Expense.model import Expense

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Total counts filtered by user
        total_events = Event.objects.filter(user=user).count()
        total_guests = Guest.objects.filter(user=user).count()
        total_records = GuestRecord.objects.filter(guest__user=user).count()
        
        # Total amounts filtered by user
        total_amount = GuestRecord.objects.filter(guest__user=user).aggregate(total=Sum('amount'))['total'] or 0
        aavel_total = GuestRecord.objects.filter(guest__user=user, select='aavel').aggregate(total=Sum('amount'))['total'] or 0
        mukel_total = GuestRecord.objects.filter(guest__user=user, select='mukel').aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = Expense.objects.filter(event__user=user).aggregate(total=Sum('amount'))['total'] or 0
        
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