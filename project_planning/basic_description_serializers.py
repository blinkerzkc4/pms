"""
-- Created by Bikash Saud
--
-- Created on 2023-06-11
"""
from rest_framework import serializers

from base_model.models import Address, CommonFieldsBase, ContactDetail, ContactPerson
from base_model.serializers import (
    AddressSerializer,
    ContactDetailSerializer,
    ContactPersonSerializer,
)
from project.models import District, FinancialYear
from project.serializers import FinancialYearSerializer, UnitSerializer
from project_planning.models import (
    ContractorType,
    DrainageType,
    ExpanseType,
    Office,
    Organization,
    OrganizationType,
    PriorityType,
    Program,
    ProjectActivity,
    ProjectLevel,
    ProjectNature,
    ProjectProcess,
    ProjectProposedType,
    ProjectStatus,
    ProjectType,
    PurchaseType,
    PurposePlan,
    Road,
    RoadStatus,
    RoadType,
    SelectionFeasibility,
    StandingList,
    StandingListType,
    StrategicSign,
    SubjectArea,
    TargetGroup,
    TargetGroupCategory,
)
from project_planning.serializers import (
    OrganizationSerializer,
    OrganizationTypeSerializer,
)


class CommonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "code", "name", "name_eng", "status", "detail")
        model = CommonFieldsBase

    def get_fields(self):
        fields = dict(super().get_fields())
        for field_name, field_class in fields.items():
            field_class.required = False
            field_class.allow_null = True
            field_class.allow_blank = True
        return fields


class ExpanseTypeSerializer(CommonSerializer):
    class Meta:
        model = ExpanseType
        fields = CommonSerializer.Meta.fields + ("is_addition",)


class ProjectTypeSerializer(CommonSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ProjectType.objects.all(), required=False
    )

    class Meta:
        model = ProjectType
        fields = CommonSerializer.Meta.fields + ("parent", "id")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        parent = instance.parent

        if parent:
            representation["parent"] = {
                "id": parent.id,
                "name": parent.name,
                "name_eng": parent.name_eng,
            }
        else:
            representation["target_group_category"] = None
        return representation


class PurposePlanSerializer(CommonSerializer):
    class Meta:
        model = PurposePlan
        fields = CommonSerializer.Meta.fields


class ProjectProcessSerializer(CommonSerializer):
    class Meta:
        model = ProjectProcess
        fields = CommonSerializer.Meta.fields


class ProjectNatureSerializer(CommonSerializer):
    class Meta:
        model = ProjectNature
        fields = CommonSerializer.Meta.fields


class ProjectLevelSerializer(CommonSerializer):
    class Meta:
        model = ProjectLevel
        fields = CommonSerializer.Meta.fields


class ProjectProposedTypeSerializer(CommonSerializer):
    class Meta:
        model = ProjectProposedType
        fields = CommonSerializer.Meta.fields


class ProjectActivitySerializer(CommonSerializer):
    class Meta:
        model = ProjectActivity
        fields = CommonSerializer.Meta.fields


class PurchaseTypeSerializer(CommonSerializer):
    class Meta:
        model = PurchaseType
        fields = CommonSerializer.Meta.fields


class PriorityTypeSerializer(CommonSerializer):
    class Meta:
        model = PriorityType
        fields = CommonSerializer.Meta.fields


class SelectionFeasibilitySerializer(CommonSerializer):
    class Meta:
        model = SelectionFeasibility
        fields = CommonSerializer.Meta.fields


class StrategicSignSerializer(CommonSerializer):
    class Meta:
        model = StrategicSign
        fields = CommonSerializer.Meta.fields


class ProgramSerializer(CommonSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Program.objects.all(), required=False
    )

    class Meta:
        model = Program
        fields = CommonSerializer.Meta.fields + ("parent",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        parent = instance.parent

        if parent:
            representation["parent"] = {
                "id": parent.id,
                "name": parent.name,
                "name_eng": parent.name_eng,
            }
        else:
            representation["target_group_category"] = None
        return representation


class TargetGroupCategorySerializer(CommonSerializer):
    class Meta:
        model = TargetGroupCategory
        fields = ("id", "name", "name_eng", "status")


class TargetGroupSerializer(CommonSerializer):
    target_group_category = serializers.PrimaryKeyRelatedField(
        queryset=TargetGroupCategory.objects.all()
    )

    class Meta:
        model = TargetGroup
        fields = CommonSerializer.Meta.fields + ("target_group_category", "karmagat")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        target_group_category = instance.target_group_category

        if target_group_category:
            representation["target_group_category"] = {
                "id": target_group_category.id,
                "name": target_group_category.name,
                "name_eng": target_group_category.name_eng,
            }
        else:
            representation["target_group_category"] = None
        return representation


class ProjectStatusSerializer(CommonSerializer):
    class Meta:
        model = ProjectStatus
        fields = CommonSerializer.Meta.fields + ("karmagat",)


class ContractorTypeSerializer(CommonSerializer):
    class Meta:
        model = ContractorType
        fields = CommonSerializer.Meta.fields + ("karmagat",)


# class DistrictSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = District
#         fields = ("id", "name", "name_eng", "status", "remarks")


class SubjectAreaSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=SubjectArea.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = SubjectArea
        fields = ("id", "code", "parent", "name", "name_eng", "status", "detail")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        parent = instance.parent

        if parent:
            representation["parent"] = {
                "id": parent.id,
                "name": parent.name,
                "name_eng": parent.name_eng,
            }
        else:
            representation["target_group_category"] = None
        return representation


class OfficeSerializer(serializers.ModelSerializer):
    organization_type = serializers.PrimaryKeyRelatedField(
        queryset=OrganizationType.objects.all(), required=True
    )
    current_address = AddressSerializer()
    former_address = AddressSerializer()
    contact_detail = ContactDetailSerializer()
    contact_person = ContactPersonSerializer()

    class Meta:
        model = Office
        fields = (
            "id",
            "organization_type",
            "code",
            "status",
            "full_name",
            "full_name_eng",
            "registration_no",
            "registration_date",
            "registration_date_eng",
            "office",
            "detail",
            "current_address",
            "former_address",
            "contact_person",
            "contact_detail",
            "remarks",
            "kramagat",
        )
        read_only_fields = ("id", "created_by")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        organization_type = instance.organization_type

        representation["organization_type"] = (
            self.get_organization_type(organization_type) if organization_type else None
        )
        return representation

    def get_organization_type(self, data):
        return {
            "id": data.id,
            "code": data.code,
            "name": data.name,
        }

    def create(self, validated_data):
        current_address_data = validated_data.pop("current_address")
        former_address_data = validated_data.pop("former_address")
        contact_detail_data = validated_data.pop("contact_detail")
        contact_person_data = validated_data.pop("contact_person")

        current_address = Address.objects.create(**current_address_data)
        former_address = Address.objects.create(**former_address_data)
        contact_detail = ContactDetail.objects.create(**contact_detail_data)
        contact_person = ContactPerson.objects.create(**contact_person_data)

        validated_data["current_address"] = current_address
        validated_data["former_address"] = former_address
        validated_data["contact_detail"] = contact_detail
        validated_data["contact_person"] = contact_person

        office_detail = Office.objects.create(**validated_data)
        return office_detail

    def update(self, instance, validated_data):
        current_address_data = validated_data.pop("current_address", None)
        former_address_data = validated_data.pop("former_address", None)
        contact_detail_data = validated_data.pop("contact_detail", None)
        contact_person_data = validated_data.pop("contact_person", None)

        if current_address_data:
            current_address_serializer = AddressSerializer(
                instance.current_address, data=current_address_data
            )
            if current_address_data["municipality"]:
                municipality = current_address_data.pop("municipality").id
                current_address_data["municipality"] = municipality

            if current_address_serializer.is_valid():
                current_address = current_address_serializer.save()
                validated_data["current_address"] = current_address

        if former_address_data:
            former_address_serializer = AddressSerializer(
                instance.former_address, data=former_address_data
            )
            if former_address_data["municipality"]:
                municipality = former_address_data.pop("municipality").id
                former_address_data["municipality"] = municipality

            if former_address_serializer.is_valid():
                former_address = former_address_serializer.save()
                validated_data["former_address"] = former_address

        if contact_detail_data:
            contact_detail_serializer = ContactDetailSerializer(
                instance.contact_detail, data=contact_detail_data
            )
            if contact_detail_serializer.is_valid():
                contact_detail = contact_detail_serializer.save()
                validated_data["contact_detail"] = contact_detail

        if contact_person_data:
            contact_person_serializer = ContactPersonSerializer(
                instance.contact_person, data=contact_person_data
            )
            if contact_person_serializer.is_valid():
                contact_person = contact_person_serializer.save()
                validated_data["contact_person"] = contact_person
        return super().update(instance, validated_data)


class StandingListTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandingListType
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        parent = instance.parent

        if parent:
            representation["parent"] = {
                "id": parent.id,
                "name": parent.name,
                "name_eng": parent.name_eng,
            }
        else:
            representation["target_group_category"] = None
        return representation


class StandingListSerializer(serializers.ModelSerializer):
    standing_list_type = serializers.PrimaryKeyRelatedField(
        queryset=StandingListType.objects.all()
    )
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all()
    )
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all()
    )

    class Meta:
        model = StandingList
        fields = (
            "id",
            "date",
            "date_eng",
            "standing_list_type",
            "registration_number",
            "organization",
            "financial_year",
            "detail",
            "status",
            "current",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        standing_list_type = instance.standing_list_type
        organization_data = instance.organization
        financial_year = instance.financial_year

        representation["standing_list_type"] = (
            self.get_common_data(standing_list_type) if standing_list_type else None
        )
        representation["organization"] = (
            self.get_organization_data(organization_data) if organization_data else None
        )
        representation["financial_year"] = (
            self.get_fy(financial_year) if financial_year else None
        )

        return representation

    def get_fy(self, data):
        return {
            "id": data.id,
            "start_year": data.start_year,
            "end_year": data.end_year,
            "fy": data.fy,
        }

    def get_common_data(self, standing_list_type):
        return {
            "id": standing_list_type.id,
            "name": standing_list_type.name,
            "name_eng": standing_list_type.name_eng,
        }

    def get_organization_data(self, data):
        return {
            "id": data.id,
            "full_name": data.full_name,
            "full_name_eng": data.full_name_eng,
            "register_no": data.register_no,
        }


class RoadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadType
        fields = "__all__"


class RoadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadStatus
        fields = "__all__"


class DrainageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrainageType
        fields = "__all__"


class RoadSerializer(serializers.ModelSerializer):
    road_type = RoadTypeSerializer(read_only=True)
    road_status = RoadStatusSerializer(read_only=True)
    road_width_unit = UnitSerializer(read_only=True)
    road_length_unit = UnitSerializer(read_only=True)
    drainage_type = DrainageTypeSerializer(read_only=True)
    drainage_width_unit = UnitSerializer(read_only=True)
    drainage_length_unit = UnitSerializer(read_only=True)

    class Meta:
        model = Road
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "road_type",
            "road_status",
            "average_width",
            "road_width_unit",
            "road_length",
            "road_length_unit",
            "connected_roads",
            "connected_wards",
            "total_consumer",
            "road_start_from",
            "road_end_to",
            "other_status",
            "karmagat",
            "drainage_exit_status",
            "drainage_type",
            "drainage_width",
            "drainage_width_unit",
            "drainage_length",
            "drainage_length_unit",
            "remarks",
            "other_remarks",
        )
