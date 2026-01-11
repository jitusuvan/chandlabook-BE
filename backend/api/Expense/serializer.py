from rest_framework import serializers
from .model import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    event_name = serializers.SerializerMethodField()
    event_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = '__all__'
        
    def get_event_name(self, obj):
        return obj.event.name if obj.event else None
        
    def get_event_date(self, obj):
        return obj.event.date if obj.event else None