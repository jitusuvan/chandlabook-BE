# serializers.py
from rest_framework import serializers
from .model import GuestRecord

class GuestRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestRecord
        fields = "__all__"
