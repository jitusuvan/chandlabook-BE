# models.py
import uuid
from django.db import models
from api.Guest.model import Guest  # FK guest table

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
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    select = models.CharField(max_length=10, choices=SELECT_TYPE)      # mukel / aavel
    event = models.CharField(max_length=10, choices=EVENT_TYPE)        # chandlo / marriage
    bride_groom = models.CharField(max_length=100, null=True, blank=True)  # only required for marriage

    def save(self, *args, **kwargs):
        if self.event != "marriage":
            self.bride_groom = None  # auto remove if not marriage
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest.first_name} - {self.event} - {self.amount}"
