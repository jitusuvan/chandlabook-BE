# serializers.py
from rest_framework import serializers
from .model import GuestRecord

class GuestRecordSerializer(serializers.ModelSerializer):
    guest_name = serializers.SerializerMethodField()
    event_name = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    
    class Meta:
        model = GuestRecord
        fields = "__all__"

    def get_guest_name(self, obj):
        if obj.guest:
            return f"{obj.guest.first_name} {obj.guest.last_name or ''} {obj.guest.surname or ''}".strip()
        return None
    
    def get_event_name(self, obj):
        return obj.event.name if obj.event else None
        
    def get_payment_status(self, obj):
        return "pending" if obj.pay_later else "paid"