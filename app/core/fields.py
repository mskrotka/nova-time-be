import time
from datetime import datetime

from django.db import models


class TimestampField(models.BigIntegerField):
    def __init__(self, *args, **kwargs):
        self.auto_now = kwargs.pop("auto_now", False)
        self.auto_now_add = kwargs.pop("auto_now_add", False)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = int(time.time() * 1000)
            setattr(model_instance, self.attname, value)
            return value
        return super().pre_save(model_instance, add)

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return int(value.timestamp() * 1000)
        if isinstance(value, (int, float)):
            return int(value)
        return super().get_prep_value(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return datetime.fromtimestamp(value / 1000)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime):
            return int(value.timestamp() * 1000)
        if isinstance(value, (int, float)):
            return int(value)
        return value
