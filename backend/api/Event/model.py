# models.py
import uuid
from django.db import models

class Event(models.Model):
    
    EVENT_TYPE = (
        ('chandlo', 'Chandlo'),
        ('marriage', 'Marriage'),
    )
    
    SELECT_TYPE = (
        ('mukel', 'Mukel'),
        ('aavel', 'Aavel'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, default='Event')
    date = models.DateField()
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE)
    select_type = models.CharField(max_length=10, choices=SELECT_TYPE)
    bride_groom_name = models.CharField(max_length=100, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.event_type != "marriage":
            self.bride_groom_name = None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.date}"
    
    class Meta:
        unique_together = ['name', 'date']