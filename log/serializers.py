from auditlog.models import LogEntry
from rest_framework import serializers

from log.models import AccessLog
from project.serializers import MunicipalitySerializer, SimpleWardSerializer
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    ward = SimpleWardSerializer(source="assigned_ward", read_only=True)
    municipality = MunicipalitySerializer(
        source="assigned_municipality", read_only=True
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        photo_uri = data["profile_picture"]
        if photo_uri:
            request = self.context.get("request")
            try:
                data["profile_picture"] = request.build_absolute_uri(photo_uri)

            except:
                data["profile_picture"] = None

        return data

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "verified",
            "ward",
            "municipality",
            "detail",
            "profile_picture",
            "last_login",
            "ip_address",
            "full_name",
            "status",
        )
        extra_kwargs = {
            "username": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
            "verified": {"required": False, "allow_null": True},
            "ward": {"required": False, "allow_null": True},
            "municipality": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
            "profile_picture": {"required": False, "allow_null": True},
            "last_login": {"required": False, "allow_null": True},
            "ip_address": {"required": False, "allow_null": True},
            "full_name": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class AccessLogSerializer(serializers.ModelSerializer):
    actor = UserSerializer()

    class Meta:
        model = AccessLog
        fields = (
            "user_id",
            "user_email",
            "username",
            "session_key",
            "path",
            "method",
            "data",
            "ip_address",
            "referer",
            "status_code",
            "created_at",
            "updated_at",
            "municipality",
            "ward",
            "status",
            "actor",
        )
        extra_kwargs = {
            "user_email": {"required": False, "allow_null": True},
            "username": {"required": False, "allow_null": True},
            "session_key": {"required": False, "allow_null": True},
            "path": {"required": False, "allow_null": True},
            "method": {"required": False, "allow_null": True},
            "data": {"required": False, "allow_null": True},
            "ip_address": {"required": False, "allow_null": True},
            "referer": {"required": False, "allow_null": True},
            "status_code": {"required": False, "allow_null": True},
            "created_at": {"required": False, "allow_null": True},
            "updated_at": {"required": False, "allow_null": True},
            "municipality": {"required": False, "allow_null": True},
            "ward": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "actor": {"required": False, "allow_null": True},
        }


class LogEntrySerializer(serializers.ModelSerializer):
    action = serializers.CharField(source="get_action_display")
    app_label = serializers.CharField(source="content_type.app_label")
    model = serializers.CharField(source="content_type.name")
    db_table = serializers.SerializerMethodField()
    actor = UserSerializer()

    class Meta:
        model = LogEntry
        fields = (
            "id",
            "object_pk",
            "object_id",
            "object_repr",
            "action",
            "remote_addr",
            "timestamp",
            "additional_data",
            "app_label",
            "model",
            "db_table",
            "changes_dict",
            "serialized_data",
            "actor",
        )
        extra_kwargs = {
            "object_pk": {"required": False, "allow_null": True},
            "object_id": {"required": False, "allow_null": True},
            "object_repr": {"required": False, "allow_null": True},
            "action": {"required": False, "allow_null": True},
            "remote_addr": {"required": False, "allow_null": True},
            "timestamp": {"required": False, "allow_null": True},
            "additional_data": {"required": False, "allow_null": True},
            "app_label": {"required": False, "allow_null": True},
            "model": {"required": False, "allow_null": True},
            "db_table": {"required": False, "allow_null": True},
            "changes_dict": {"required": False, "allow_null": True},
            "serialized_data": {"required": False, "allow_null": True},
            "actor": {"required": False, "allow_null": True},
        }

    def get_db_table(self, obj):
        return obj.content_type.model_class()._meta.db_table
