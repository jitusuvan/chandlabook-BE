# serializers.py
from rest_framework import serializers
from api.Guest.model import Guest

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        # Prevent clients from creating/updating objects for other users.
        read_only_fields = ("user",)
        fields = '__all__'

