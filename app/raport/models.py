import uuid

from django.db import models


class Task(models.Model):
    id = models.CharField(
        primary_key=True, max_length=128, default=uuid.uuid4, editable=False
    )

    jira_id = models.CharField(max_length=128, unique=True, db_index=True)
    title = models.CharField(max_length=512)

    def __str__(self) -> str:
        return f"{self.jira_id}: {self.title}"


class TimeTracking(models.Model):
    id = models.CharField(
        primary_key=True, max_length=128, default=uuid.uuid4, editable=False
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="time_trackings",
        db_index=True,
    )

    duration_seconds = models.PositiveIntegerField()

    # timestamp w milisekundach (Unix epoch ms)
    start_ms = models.BigIntegerField()
    end_ms = models.BigIntegerField()

    def __str__(self) -> str:
        return f"{self.task.jira_id} ({self.duration_seconds}s)"
