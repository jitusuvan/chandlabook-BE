# models.py
import uuid
from django.db import models

class Guest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    mobile_no = models.CharField(max_length=15, unique=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}"
