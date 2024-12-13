from django.db import models

# Create your models here.
from project.models import BaseModel
from user.models import User


class Notification(BaseModel):
    title = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(
        "plan_execution.ProjectExecution",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    official_process = models.ForeignKey(
        "plan_execution.OfficialProcess",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    notified_for = models.CharField(max_length=100, null=True, blank=True)
    notified_object = models.JSONField(null=True, blank=True)
    link = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="notification_for",
    )
    is_read = models.BooleanField(default=False)
    status = models.BooleanField(default=True, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
