import uuid

from django.db import models
from simple_history.models import HistoricalRecords

from .fields import TimestampField

# Create your models here.


class BaseModel(models.Model):
    id = models.CharField(
        primary_key=True, max_length=128, default=uuid.uuid4, editable=False
    )
    created = TimestampField(auto_now_add=True, editable=False)
    modified = TimestampField(auto_now=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
