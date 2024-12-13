"""
-- Created by Bikash Saud
--
-- Created on 2023-06-07
"""

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import exceptions, serializers

from base_model.base_serializers import WriteableNestedModelBaseSerializer
from base_model.utils import get_relation_id
from project.models import Municipality
from project.serializers import SimpleMunicipalitySerializer

from .models import Address, ContactDetail, ContactPerson, Gender


class GenderSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get("name", None) is None and attrs.get("name_eng", None) is None:
            raise exceptions.ValidationError(
                {
                    "name": "Either enter name or english name",
                    "name_eng": "Either enter name or english name",
                }
            )

        return super().validate(attrs)

    class Meta:
        model = Gender
        fields = ("id", "name", "name_eng", "status", "detail")
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }


class AddressSerializer(WritableNestedModelSerializer):
    municipality = serializers.PrimaryKeyRelatedField(
        queryset=Municipality.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Address
        fields = (
            "id",
            "municipality",
            "ward",
            "ward_eng",
            "house_no",
            "tole_eng",
            "village_name",
            "road_name",
            "road_name_eng",
            "status",
        )
        extra_kwargs = {
            "ward": {"required": False, "allow_null": True},
            "ward_eng": {"required": False, "allow_null": True},
            "house_no": {"required": False, "allow_null": True},
            "tole_eng": {"required": False, "allow_null": True},
            "road_name": {"required": False, "allow_null": True},
            "road_name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_internal_value(self, data):
        updated_data = self.correct_data(data)
        return super().to_internal_value(updated_data)

    @staticmethod
    def correct_data(address_data: dict) -> dict:
        if address_data:
            address_data["municipality"] = get_relation_id(address_data, "municipality")
        return address_data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["municipality"] = (
            SimpleMunicipalitySerializer(instance.municipality).data
            if instance.municipality
            else None
        )
        return ret


class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = (
            "id",
            "phone_number",
            "mobile_number",
            "fax_number",
            "email",
            "mailing_address",
            "status",
        )
        extra_kwargs = {
            "phone_number": {"required": False, "allow_null": True},
            "mobile_number": {"required": False, "allow_null": True},
            "fax_number": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
            "mailing_address": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = (
            "id",
            "name",
            "name_eng",
            "position",
            "phone_number",
            "mobile_number",
            "email",
            "remark",
            "kramagat",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False},
            "name_eng": {"required": False},
            "position": {"required": False},
            "phone_number": {"required": False},
            "mobile_number": {"required": False},
            "email": {"required": False},
            "remark": {"required": False},
            "kramagat": {"required": False},
            "status": {"required": False},
        }
