from django.conf import settings
from django.db import models

from project.models import BaseModel, Municipality, Ward

# Create your models here.


class AccessLog(BaseModel):
    user_id = models.BigIntegerField(null=True, default=0, blank=True)
    user_email = models.EmailField(blank=True)
    username = models.CharField(max_length=255, blank=True)
    session_key = models.CharField(max_length=1024, null=True, blank=True)
    path = models.CharField(max_length=1024, blank=True, null=True)
    method = models.CharField(max_length=10, blank=True, null=True)
    data = models.JSONField(null=True, blank=True)
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    referer = models.CharField(max_length=512, null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    municipality = models.ForeignKey(
        Municipality, null=True, blank=True, on_delete=models.PROTECT
    )
    ward = models.ForeignKey(Ward, null=True, blank=True, on_delete=models.PROTECT)
    status = models.BooleanField(default=True, null=True, blank=True)
    actor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="access_logs",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "log"
        verbose_name = "Access Log"
        verbose_name_plural = "Access Logs"
        ordering = ("-created_at",)
