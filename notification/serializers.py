"""
-- Created by Bikash Saud
-- Created on 2023-08-25
"""
import nepali_datetime
from rest_framework import serializers

from pms_system import settings
from pms_system.settings import MEDIA_URL
from utils.constants import ProcessStatus, RequestSend
from utils.nepali_date import ad_to_bs

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "title",
            "description",
            "project",
            "official_process",
            "link",
            "user",
            "is_read",
            "status",
            "notified_for",
            "notified_object",
        )
        extra_kwargs = {
            "title": {"required": False, "allow_null": True},
            "description": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "official_process": {"required": False, "allow_null": True},
            "link": {"required": False, "allow_null": True},
            "user": {"required": False, "allow_null": True},
            "is_read": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "notified_for": {"required": False, "allow_null": True},
            "notified_object": {"required": False, "allow_null": True},
        }
    def to_representation(self, instance):
        data = super().to_representation(instance)
        official_process = instance.official_process
        project = instance.project
        user = instance.user
        created_at = instance.created_date
        if official_process:
            op_data = {
                "request_by": self.get_user(official_process.request_by)
                if official_process.request_by
                else None,
                "send_to": self.get_user(official_process.send_to)
                if official_process.send_to
                else None,
                "send_for": self.get_request_type(official_process.send_for)
                if official_process.send_for
                else None,
                "status": self.get_status(official_process.status)
                if official_process.status
                else None,
                "file": self.get_file(official_process.file)
                if official_process.file
                else None,
                "feedback_file": self.get_file(official_process.feedback_file)
                if official_process.feedback_file
                else None,
                "remarks": official_process.remarks,
                "feedback_remarks": official_process.feedback_remarks,
            }
        else:
            op_data = None
        data["official_process"] = op_data
        if project:
            data["project"] = self.get_project_data(project) if project else None
        else:
            data["project"] = None
        data["user"] = self.get_user(user) if user else None
        np_date = ad_to_bs(created_at.date())
        data["date"] = str(np_date)
        return data

    def get_file(self, data):
        return f"{settings.SITE_HOST}{MEDIA_URL}{data}"

    @staticmethod
    def get_user(data):
        return {
            "id": data.id,
            "username": data.username,
            "full_name": f"{data.first_name} {data.last_name}",
            "email": data.email,
        }

    def get_request_type(self, data):
        return {"value": data, "label": RequestSend(data).label}

    def get_status(self, data):
        return {"value": data, "label": ProcessStatus(data).label}

    def get_project_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
        }
