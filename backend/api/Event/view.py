from rest_framework import generics, status
from rest_framework.response import Response
from .model import Event
from .serializer import EventSerializer

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer