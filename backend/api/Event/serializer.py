from rest_framework import serializers
from django.db.models import Sum
from .model import Event

class EventSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = '__all__'
        
    def get_total_amount(self, obj):
        return obj.event_guestRecord_FK.aggregate(total=Sum('amount'))['total'] or 0
        
    def validate(self, data):
        if data.get('event_type') == 'marriage' and not data.get('bride_groom_name'):
            raise serializers.ValidationError("Bride/Groom name is required for marriage events")
        return data