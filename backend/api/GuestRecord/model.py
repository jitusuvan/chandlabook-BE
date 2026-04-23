import uuid
from django.db import models
from api.Guest.model import Guest  # FK guest table
from api.Event.model import Event  # FK event table

class GuestRecord(models.Model):

    SELECT_TYPE = (
        ('mukel', 'Mukel'),
        ('aavel', 'Aavel'),
    )

    EVENT_TYPE = (
        ('chandlo', 'Chandlo'),
        ('marriage', 'Marriage'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey(Guest, related_name="guest_guestRecord_FK", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="event_guestRecord_FK", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    select = models.CharField(max_length=10, choices=SELECT_TYPE)      # mukel / aavel
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE, default='chandlo')        # chandlo / marriage
    bride_groom = models.CharField(max_length=100, null=True, blank=True)  # only required for marriage
    pay_later = models.BooleanField(default=False)

    class Meta:
        unique_together = ['guest', 'event', 'date', 'amount', 'select']

    def save(self, *args, **kwargs):
        # If event is selected, copy values from event
        if self.event:
            self.date = self.event.date
            self.event_type = self.event.event_type
            self.select = self.event.select_type
            self.bride_groom = self.event.bride_groom_name
        
        # Auto remove bride_groom if not marriage
        if self.event_type != "marriage":
            self.bride_groom = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest.first_name} - {self.event_type} - {self.amount}"
