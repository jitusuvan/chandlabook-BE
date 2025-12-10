# serializers.py
from rest_framework import serializers
from api.Guest.model import Guest

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'
