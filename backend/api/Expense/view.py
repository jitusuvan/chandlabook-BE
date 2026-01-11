from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .model import Expense
from .serializer import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-created_at')
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']