from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers, exceptions

from base_model.models import CommonFieldsBase


class WriteableNestedModelBaseSerializer(WritableNestedModelSerializer):
    def get_fields(self):
        fields = dict(super().get_fields())
        for field_name, field_class in fields.items():
            field_class.required = False
            field_class.allow_null = True
            field_class.allow_blank = True
        return fields

    def get_common_data(self, data):
        if not data:
            return None
        return {
            "id": data.id,
            "name": str(data.name),
            "name_eng": str(data.name_eng),
            "code": str(data.code),
        }


class BaseSerializer(serializers.ModelSerializer):
    municipality_field_name = "municipality"

    def save(self, **kwargs):
        manipulation_data = {}
        object_ownership_data = {}
        request = self.context.get("request")
        if request:
            if not self.instance:
                manipulation_data["created_by"] = request.user
            manipulation_data["updated_by"] = request.user

            field_names = dict(self.get_fields()).keys()
            if self.municipality_field_name in field_names:
                object_ownership_data[
                    "municipality"
                ] = request.user.assigned_municipality

        return super().save(**{**kwargs, **manipulation_data, **object_ownership_data})

    def get_fields(self):
        fields = dict(super().get_fields())
        for field_name, field_class in fields.items():
            field_class.required = False
            field_class.allow_null = True
            field_class.allow_blank = True
        return fields

    def get_common_data(self, data):
        if not data:
            return None
        return {
            "id": data.id,
            "name": str(data.name),
            "name_eng": str(data.name_eng),
            "code": str(data.code),
        }


class CommonSerializer(BaseSerializer):
    def validate(self, attrs, validate_name=True):
        if (
            validate_name
            and attrs.get("name", None) is None
            and attrs.get("name_eng", None) is None
        ):
            raise exceptions.ValidationError(
                {
                    "name": "Either enter name or english name",
                    "name_eng": "Either enter name or english name",
                }
            )

        if attrs.get("code", None) is None:
            raise exceptions.ValidationError({"code": "This cannot be null"})

        return super().validate(attrs)

    class Meta:
        fields = ("id", "code", "name", "name_eng", "status", "detail")
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }
        model = CommonFieldsBase
