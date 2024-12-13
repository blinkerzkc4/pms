"""
-- Created by Bikash Saud
--
-- Created on 2023-06-07
"""

from rest_framework import exceptions, serializers

from base_model.models import Address, CommonFieldsBase, ContactDetail, Gender
from base_model.serializers import (
    AddressSerializer,
    ContactDetailSerializer,
    GenderSerializer,
)
from base_model.base_serializers import BaseSerializer
from base_model.utils import get_relation_id
from project_planning.basic_description_serializers import SubjectAreaSerializer
from project_planning.models import BFI, PaymentMedium, SubjectArea
from project_planning.serializers import BFISerializer, PaymentMediumSerializer

from .models import (
    Country,
    CumulativeDetail,
    CurrentWorkingDetail,
    Department,
    DepartmentBranch,
    Employee,
    EmployeeSector,
    EmployeeType,
    EnrollmentDetail,
    FamilyDetail,
    Language,
    MaritalStatus,
    Nationality,
    Position,
    PositionLevel,
    PublicRepresentativeDetail,
    PublicRepresentativePosition,
    Religion,
    ServiceGroup,
    TaxPayer,
)


class CommonSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get("name", None) is None and attrs.get("name_eng", None) is None:
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

    def get_fields(self):
        fields = dict(super().get_fields())
        for field_name, field_class in fields.items():
            field_class.required = False
            field_class.allow_null = True
            field_class.allow_blank = True
        return fields


class MaritalStatusSerializer(CommonSerializer):
    class Meta:
        fields = CommonSerializer.Meta.fields
        model = MaritalStatus


class DepartmentSerializer(CommonSerializer):
    class Meta:
        fields = CommonSerializer.Meta.fields
        model = Department


class DepartmentBranchSerializer(CommonSerializer):
    class Meta:
        fields = CommonSerializer.Meta.fields
        model = DepartmentBranch


class PositionLevelSerializer(CommonSerializer):
    class Meta:
        fields = "__all__"
        model = PositionLevel


class PositionSerializer(CommonSerializer):
    class Meta:
        fields = CommonSerializer.Meta.fields
        model = Position


class EmployeeTypeSerializer(CommonSerializer):
    class Meta:
        fields = CommonSerializer.Meta.fields
        model = EmployeeType


class ServiceGroupSerializer(CommonSerializer):
    class Meta:
        fields = CommonSerializer.Meta.fields
        model = ServiceGroup


class EmployeeSectorSerializer(CommonSerializer):
    position_level = serializers.PrimaryKeyRelatedField(
        queryset=PositionLevel.objects.all(), required=False, allow_null=True
    )
    position = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), required=False, allow_null=True
    )

    class Meta:
        fields = "__all__"
        model = EmployeeSector

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        position_level = instance.position_level
        position = instance.position
        representation["position_level"] = (
            PositionLevelSerializer(position_level).data if position_level else {}
        )
        representation["position"] = (
            PositionSerializer(position).data if position else {}
        )
        return representation


class CurrentWorkingDetailSerializer(BaseSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )
    department_branch = serializers.PrimaryKeyRelatedField(
        queryset=DepartmentBranch.objects.all(), required=False, allow_null=True
    )
    position_level = serializers.PrimaryKeyRelatedField(
        queryset=PositionLevel.objects.all(), required=False, allow_null=True
    )
    work_area = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), required=False, allow_null=True
    )
    employee_type = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeType.objects.all(), required=False, allow_null=True
    )
    service_group = serializers.PrimaryKeyRelatedField(
        queryset=ServiceGroup.objects.all(), required=False, allow_null=True
    )
    position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    payment_medium = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMedium.objects.all(), required=False, allow_null=True
    )
    bank_name = serializers.PrimaryKeyRelatedField(
        queryset=BFI.objects.all(), required=False, allow_null=True
    )

    @staticmethod
    def correct_data(cwd_data: dict) -> dict:
        if cwd_data:
            cwd_data["department"] = get_relation_id(cwd_data, "department")
            cwd_data["department_branch"] = get_relation_id(
                cwd_data, "department_branch"
            )
            cwd_data["position_level"] = get_relation_id(cwd_data, "position_level")
            cwd_data["work_area"] = get_relation_id(cwd_data, "work_area")
            cwd_data["employee_type"] = get_relation_id(cwd_data, "employee_type")
            cwd_data["service_group"] = get_relation_id(cwd_data, "service_group")
            cwd_data["position"] = get_relation_id(cwd_data, "position")
            cwd_data["payment_medium"] = get_relation_id(cwd_data, "payment_medium")
            cwd_data["bank_name"] = get_relation_id(cwd_data, "bank_name")
        return cwd_data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["department"] = self.get_common_data(instance.department)
        rep["department_branch"] = self.get_common_data(instance.department_branch)
        rep["position_level"] = self.get_common_data(instance.position_level)
        rep["work_area"] = self.get_common_data(instance.work_area)
        rep["employee_type"] = self.get_common_data(instance.employee_type)
        rep["service_group"] = self.get_common_data(instance.service_group)
        rep["position"] = self.get_common_data(instance.position)
        rep["payment_medium"] = self.get_common_data(instance.payment_medium)
        rep["bank_name"] = self.get_common_data(instance.bank_name)
        return rep

    class Meta:
        model = CurrentWorkingDetail
        fields = (
            "id",
            "department",
            "department_branch",
            "position",
            "position_level",
            "employee_type",
            "work_area",
            "retirement_date",
            "service_group",
            "retirement_date_eng",
            "leave_date",
            "leave_date_eng",
            "insurance_facility",
            "penalty_deduction",
            "payment_medium",
            "bank_name",
            "bank_sheet_no",
            "account_no",
            "remarks",
            "kramagat",
            "condition",
            "status",
        )
        extra_kwargs = {
            "department": {"required": False, "allow_null": True},
            "department_branch": {"required": False, "allow_null": True},
            "position": {"required": False, "allow_null": True},
            "position_level": {"required": False, "allow_null": True},
            "employee_type": {"required": False, "allow_null": True},
            "work_area": {"required": False, "allow_null": True},
            "retirement_date": {"required": False, "allow_null": True},
            "service_group": {"required": False, "allow_null": True},
            "retirement_date_eng": {"required": False, "allow_null": True},
            "leave_date": {"required": False, "allow_null": True},
            "leave_date_eng": {"required": False, "allow_null": True},
            "insurance_facility": {"required": False, "allow_null": True},
            "penalty_deduction": {"required": False, "allow_null": True},
            "payment_medium": {"required": False, "allow_null": True},
            "bank_name": {"required": False, "allow_null": True},
            "bank_sheet_no": {"required": False, "allow_null": True},
            "account_no": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "kramagat": {"required": False, "allow_null": True},
            "condition": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class FamilyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyDetail
        fields = (
            "father_name",
            "father_name_eng",
            "mother_name",
            "mother_name_eng",
            "spouse_name",
            "spouse_name_eng",
            "wished_person_name",
            "wished_person_name_eng",
            "status",
        )
        extra_kwargs = {
            "father_name": {"required": False, "allow_null": True},
            "father_name_eng": {"required": False, "allow_null": True},
            "mother_name": {"required": False, "allow_null": True},
            "mother_name_eng": {"required": False, "allow_null": True},
            "spouse_name": {"required": False, "allow_null": True},
            "spouse_name_eng": {"required": False, "allow_null": True},
            "wished_person_name": {"required": False, "allow_null": True},
            "wished_person_name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class EnrollmentDetailSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )
    position = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = EnrollmentDetail
        fields = (
            "department",
            "position",
            "start_date",
            "end_date",
            "status",
        )
        extra_kwargs = {
            "department": {"required": False, "allow_null": True},
            "position": {"required": False, "allow_null": True},
            "start_date": {"required": False, "allow_null": True},
            "end_date": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    @staticmethod
    def correct_data(enrollment_data: dict) -> dict:
        if enrollment_data:
            enrollment_data["department"] = get_relation_id(
                enrollment_data, "department"
            )
            enrollment_data["position"] = get_relation_id(enrollment_data, "position")
        return enrollment_data

    def update(self, instance, validated_data):
        department = validated_data.pop("department")
        position = validated_data.pop("position")

        if department:
            department_serializer = DepartmentSerializer(
                instance=instance.department, data=department
            )
            department_serializer.is_valid(raise_exception=True)
            department = department_serializer.save()
            validated_data["department"] = department

        if position:
            position_serializer = PositionSerializer(
                instance=instance.position, data=position
            )
            position_serializer.is_valid(raise_exception=True)
            position = position_serializer.save()
            validated_data["position"] = position

        return super().update(instance, validated_data)


class CumulativeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CumulativeDetail
        fields = (
            "book_store_no",
            "employee_saving_funds_no",
            "permanent_article_no",
            "citizen_investment_no",
            "cif_certificate_no",
            "citizen_investment_deduction_percent",
            "insurance_company",
            "insurance_policy_no",
            "insurance_amount",
            "status",
        )
        extra_kwargs = {
            "book_store_no": {"required": False, "allow_null": True},
            "employee_saving_funds_no": {"required": False, "allow_null": True},
            "permanent_article_no": {"required": False, "allow_null": True},
            "citizen_investment_no": {"required": False, "allow_null": True},
            "cif_certificate_no": {"required": False, "allow_null": True},
            "citizen_investment_deduction_percent": {
                "required": False,
                "allow_null": True,
            },
            "insurance_company": {"required": False, "allow_null": True},
            "insurance_policy_no": {"required": False, "allow_null": True},
            "insurance_amount": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class EmployeeSerializer(BaseSerializer):
    gender = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.all(), required=False, allow_null=True
    )
    marital_status = serializers.PrimaryKeyRelatedField(
        queryset=MaritalStatus.objects.all(), required=False, allow_null=True
    )
    subject_area = serializers.PrimaryKeyRelatedField(
        queryset=SubjectArea.objects.all(), required=False, allow_null=True
    )
    permanent_address = AddressSerializer(required=False, allow_null=True)
    temporary_address = AddressSerializer(required=False, allow_null=True)
    current_working_details = CurrentWorkingDetailSerializer(
        required=False, allow_null=True
    )
    family_detail = FamilyDetailSerializer(required=False, allow_null=True)
    enrollment_detail = EnrollmentDetailSerializer(required=False, allow_null=True)
    cumulative_detail = CumulativeDetailSerializer(required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = (
            "id",
            "code",
            "first_name",
            "first_name_eng",
            "middle_name",
            "middle_name_eng",
            "last_name",
            "last_name_eng",
            "dob",
            "dob_eng",
            "gender",
            "contact_number",
            "phone_number",
            "email",
            "image",
            "marital_status",
            "subject_area",
            "permanent_address",
            "temporary_address",
            "current_working_details",
            "family_detail",
            "enrollment_detail",
            "cumulative_detail",
            "created_by",
            "created_date",
            "status",
            "updated_date",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "first_name": {"required": False, "allow_null": True},
            "first_name_eng": {"required": False, "allow_null": True},
            "middle_name": {"required": False, "allow_null": True},
            "middle_name_eng": {"required": False, "allow_null": True},
            "last_name": {"required": False, "allow_null": True},
            "last_name_eng": {"required": False, "allow_null": True},
            "dob": {"required": False, "allow_null": True},
            "dob_eng": {"required": False, "allow_null": True},
            "gender": {"required": False, "allow_null": True},
            "contact_number": {"required": False, "allow_null": True},
            "phone_number": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
            "image": {"required": False, "allow_null": True},
            "marital_status": {"required": False, "allow_null": True},
            "subject_area": {"required": False, "allow_null": True},
            "permanent_address": {"required": False, "allow_null": True},
            "temporary_address": {"required": False, "allow_null": True},
            "current_working_details": {"required": False, "allow_null": True},
            "family_detail": {"required": False, "allow_null": True},
            "enrollment_detail": {"required": False, "allow_null": True},
            "cumulative_detail": {"required": False, "allow_null": True},
            "created_by": {"required": False, "allow_null": True},
            "created_date": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "updated_date": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        permanent_address_data = validated_data.pop("permanent_address")
        temporary_address_data = validated_data.pop("temporary_address")
        current_working_detail_data = validated_data.pop("current_working_details")
        family_detail_data = validated_data.pop("family_detail")
        enrollment_details_data = validated_data.pop("enrollment_detail")
        cumulative_details_data = validated_data.pop("cumulative_detail")

        permanent_address = Address.objects.create(**permanent_address_data)
        temporary_address = Address.objects.create(**temporary_address_data)

        current_working_detail = CurrentWorkingDetail.objects.create(
            **current_working_detail_data
        )

        family_detail = FamilyDetail.objects.create(**family_detail_data)
        enrollment_detail = EnrollmentDetail.objects.create(**enrollment_details_data)
        cumulative_detail = CumulativeDetail.objects.create(**cumulative_details_data)

        employee_detail = Employee.objects.create(
            permanent_address=permanent_address,
            temporary_address=temporary_address,
            family_detail=family_detail,
            enrollment_detail=enrollment_detail,
            cumulative_detail=cumulative_detail,
            current_working_details=current_working_detail,
            **validated_data,
        )

        return employee_detail

    def update(self, instance, validated_data):
        permanent_address_data = validated_data.pop("permanent_address", None)
        temporary_address_data = validated_data.pop("temporary_address", None)
        current_working_detail_data = validated_data.pop(
            "current_working_details", None
        )
        family_detail_data = validated_data.pop("family_detail", None)
        enrollment_detail_data = validated_data.pop("enrollment_detail", None)
        cumulative_detail_data = validated_data.pop("cumulative_detail", None)

        if permanent_address_data:
            permanent_address_serializer = AddressSerializer(
                instance.permanent_address,
                data=AddressSerializer.correct_data(permanent_address_data),
            )
            if permanent_address_serializer.is_valid():
                permanent_address = permanent_address_serializer.save()
                validated_data["permanent_address"] = permanent_address

        if temporary_address_data:
            temporary_address_serializer = AddressSerializer(
                instance.temporary_address,
                data=AddressSerializer.correct_data(temporary_address_data),
            )

            if temporary_address_serializer.is_valid():
                temporary_address = temporary_address_serializer.save()
                validated_data["temporary_address"] = temporary_address

        if current_working_detail_data:
            current_working_detail_serializer = CurrentWorkingDetailSerializer(
                instance.current_working_details,
                data=CurrentWorkingDetailSerializer.correct_data(
                    current_working_detail_data
                ),
            )
            if current_working_detail_serializer.is_valid():
                current_working_detail = current_working_detail_serializer.save()
                validated_data["current_working_detail"] = current_working_detail
            else:
                print(current_working_detail_serializer.errors, "Error to get data")
        if family_detail_data:
            family_detail_serializer = FamilyDetailSerializer(
                instance.family_detail, data=family_detail_data
            )
            if family_detail_serializer.is_valid():
                family_detail = family_detail_serializer.save()
                validated_data["family_detail"] = family_detail

        if enrollment_detail_data:
            enrollment_detail_serializer = EnrollmentDetailSerializer(
                instance.enrollment_detail,
                data=EnrollmentDetailSerializer.correct_data(enrollment_detail_data),
            )
            if enrollment_detail_serializer.is_valid():
                enrollment_detail = enrollment_detail_serializer.save()
                validated_data["enrollment_detail"] = enrollment_detail
            else:
                print(
                    f"error to update enrollment detail: {enrollment_detail_serializer.errors}"
                )

        if cumulative_detail_data:
            cumulative_detail_serializer = CumulativeDetailSerializer(
                instance.cumulative_detail, data=cumulative_detail_data
            )
            if cumulative_detail_serializer.is_valid():
                cumulative_detail = cumulative_detail_serializer.save()
                validated_data["cumulative_detail"] = cumulative_detail

        return super().update(instance, validated_data)


class EmployeeViewSerializer(BaseSerializer):
    gender = GenderSerializer(required=False, allow_null=True)
    marital_status = MaritalStatusSerializer(required=False, allow_null=True)
    subject_area = SubjectAreaSerializer(required=False, allow_null=True)
    permanent_address = AddressSerializer(required=False, allow_null=True)
    temporary_address = AddressSerializer(required=False, allow_null=True)
    current_working_details = CurrentWorkingDetailSerializer(
        required=False, allow_null=True
    )
    family_detail = FamilyDetailSerializer(required=False, allow_null=True)
    enrollment_detail = EnrollmentDetailSerializer(required=False, allow_null=True)
    cumulative_detail = CumulativeDetailSerializer(required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = "__all__"

    def get_gender(self, obj):
        if obj.gender:
            return GenderSerializer(obj.gender).data
        return None

    def get_material_status(self, obj):
        if obj.material_status:
            return MaritalStatusSerializer(obj.material_status).data
        return None

    def get_subject_area(self, obj):
        if obj.subject_area:
            return SubjectAreaSerializer(obj.subject_area).data
        return None

    def get_permanent_address(self, obj):
        if obj.permanent_address:
            return AddressSerializer(obj.permanent_address).data
        return None

    def get_temporary_address(self, obj):
        if obj.temporary_address:
            return AddressSerializer(obj.temporary_address).data
        return None

    def get_current_working_details(self, obj):
        if obj.current_working_details:
            return CurrentWorkingDetailSerializer(obj.current_working_details).data
        return None

    def get_family_detail(self, obj):
        if obj.family_detail:
            return FamilyDetailSerializer(obj.family_detail).data
        return None

    def get_enrollment_detail(self, obj):
        if obj.enrollment_detail:
            return EnrollmentDetailSerializer(obj.enrollment_detail).data
        return None

    def get_cumulative_detail(self, obj):
        if obj.cumulative_detail:
            return CumulativeDetailSerializer(obj.cumulative_detail).data
        return None


class ReligionSerializer(CommonSerializer):
    class Meta:
        model = Religion
        fields = CommonSerializer.Meta.fields


class LanguageSerializer(CommonSerializer):
    class Meta:
        model = Language
        fields = CommonSerializer.Meta.fields


class CountrySerializer(CommonSerializer):
    class Meta:
        model = Country
        fields = CommonSerializer.Meta.fields


class NationalitySerializer(CommonSerializer):
    class Meta:
        model = Nationality
        fields = CommonSerializer.Meta.fields


class TaxPayerSerializer(serializers.ModelSerializer):
    gender = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = TaxPayer
        fields = (
            "id",
            "status",
            "tax_payer_no",
            "internal_source_no",
            "tax_payer_name",
            "citizenship_no",
            "citizenship_from",
            "citizenship_register_date",
            "registration_no",
            "permanent_address",
            "gender",
            "dob",
            "contact_no",
            "language",
            "text_payer_type",
        )
        extra_kwargs = {
            "status": {"required": False, "allow_null": True},
            "tax_payer_no": {"required": False, "allow_null": True},
            "internal_source_no": {"required": False, "allow_null": True},
            "tax_payer_name": {"required": False, "allow_null": True},
            "citizenship_no": {"required": False, "allow_null": True},
            "citizenship_from": {"required": False, "allow_null": True},
            "citizenship_register_date": {"required": False, "allow_null": True},
            "registration_no": {"required": False, "allow_null": True},
            "permanent_address": {"required": False, "allow_null": True},
            "gender": {"required": False, "allow_null": True},
            "dob": {"required": False, "allow_null": True},
            "contact_no": {"required": False, "allow_null": True},
            "language": {"required": False, "allow_null": True},
            "text_payer_type": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        gender = instance.gender
        representation["gender"] = self.get_common_data(gender) if gender else None
        return representation

    def get_common_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
        }


class PublicRepresentativePositionSerializer(CommonSerializer):
    class Meta:
        model = PublicRepresentativePosition
        fields = CommonSerializer.Meta.fields


class PublicRepresentativeDetailSerializer(serializers.ModelSerializer):
    representative_position = serializers.PrimaryKeyRelatedField(
        queryset=PublicRepresentativePosition.objects.all(),
        required=False,
        allow_null=True,
    )
    tax_payer = serializers.PrimaryKeyRelatedField(
        queryset=TaxPayer.objects.all(), required=False, allow_null=True
    )
    religion = serializers.PrimaryKeyRelatedField(
        queryset=Religion.objects.all(), required=False, allow_null=True
    )
    language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), required=False, allow_null=True
    )
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), required=False, allow_null=True
    )
    nationality = serializers.PrimaryKeyRelatedField(
        queryset=Nationality.objects.all(), required=False, allow_null=True
    )
    permanent_current_address = AddressSerializer(required=False, allow_null=True)
    permanent_former_address = AddressSerializer(required=False, allow_null=True)
    temporary_current_address = AddressSerializer(required=False, allow_null=True)
    temporary_former_address = AddressSerializer(required=False, allow_null=True)
    contact_details = ContactDetailSerializer(required=False, allow_null=True)

    class Meta:
        model = PublicRepresentativeDetail
        fields = (
            "id",
            "status",
            "representative_position",
            "tax_payer",
            "tax_payer_type",
            "first_name",
            "middle_name",
            "last_name",
            "father_name",
            "grand_father_name",
            "first_name_eng",
            "middle_name_eng",
            "last_name_eng",
            "father_name_eng",
            "grand_father_name_eng",
            "dob",
            "dob_eng",
            "religion",
            "language",
            "country",
            "nationality",
            "citizenship_no",
            "citizenship_start_date",
            "citizenship_start_date_eng",
            "citizenship_from",
            "passport",
            "passport_start_date",
            "passport_start_date_eng",
            "passport_start_district",
            "voter_no",
            "voter_start_date",
            "voter_start_date_eng",
            "permanent_acc_no",
            "other_detail",
            "permanent_current_address",
            "permanent_former_address",
            "temporary_current_address",
            "temporary_former_address",
            "contact_details",
            "position",
            "position_level",
            "position_start_date",
            "position_start_date_eng",
            "position_end_date",
            "position_end_date_eng",
            "remarks",
            "karmagat",
        )
        extra_kwargs = {
            "status": {"required": False, "allow_null": True},
            "representative_position": {"required": False, "allow_null": True},
            "tax_payer": {"required": False, "allow_null": True},
            "tax_payer_type": {"required": False, "allow_null": True},
            "first_name": {"required": False, "allow_null": True},
            "middle_name": {"required": False, "allow_null": True},
            "last_name": {"required": False, "allow_null": True},
            "father_name": {"required": False, "allow_null": True},
            "grand_father_name": {"required": False, "allow_null": True},
            "first_name_eng": {"required": False, "allow_null": True},
            "middle_name_eng": {"required": False, "allow_null": True},
            "last_name_eng": {"required": False, "allow_null": True},
            "father_name_eng": {"required": False, "allow_null": True},
            "grand_father_name_eng": {"required": False, "allow_null": True},
            "dob": {"required": False, "allow_null": True},
            "dob_eng": {"required": False, "allow_null": True},
            "religion": {"required": False, "allow_null": True},
            "language": {"required": False, "allow_null": True},
            "country": {"required": False, "allow_null": True},
            "nationality": {"required": False, "allow_null": True},
            "citizenship_no": {"required": False, "allow_null": True},
            "citizenship_start_date": {"required": False, "allow_null": True},
            "citizenship_start_date_eng": {"required": False, "allow_null": True},
            "citizenship_from": {"required": False, "allow_null": True},
            "passport": {"required": False, "allow_null": True},
            "passport_start_date": {"required": False, "allow_null": True},
            "passport_start_date_eng": {"required": False, "allow_null": True},
            "passport_start_district": {"required": False, "allow_null": True},
            "voter_no": {"required": False, "allow_null": True},
            "voter_start_date": {"required": False, "allow_null": True},
            "voter_start_date_eng": {"required": False, "allow_null": True},
            "permanent_acc_no": {"required": False, "allow_null": True},
            "other_detail": {"required": False, "allow_null": True},
            "permanent_current_address": {"required": False, "allow_null": True},
            "permanent_former_address": {"required": False, "allow_null": True},
            "temporary_current_address": {"required": False, "allow_null": True},
            "temporary_former_address": {"required": False, "allow_null": True},
            "contact_details": {"required": False, "allow_null": True},
            "position": {"required": False, "allow_null": True},
            "position_level": {"required": False, "allow_null": True},
            "position_start_date": {"required": False, "allow_null": True},
            "position_start_date_eng": {"required": False, "allow_null": True},
            "position_end_date": {"required": False, "allow_null": True},
            "position_end_date_eng": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "karmagat": {"required": False, "allow_null": True},
        }

    read_only_fields = ("id",)

    def create(self, validated_data):
        permanent_current_address_data = validated_data.pop("permanent_current_address")
        permanent_former_address_data = validated_data.pop("permanent_former_address")
        temporary_current_address_data = validated_data.pop("temporary_current_address")
        temporary_former_address_data = validated_data.pop("temporary_former_address")
        contact_details_data = validated_data.pop("contact_details")

        permanent_current_address = Address.objects.create(
            **permanent_current_address_data
        )
        permanent_former_address = Address.objects.create(
            **permanent_former_address_data
        )
        temporary_current_address = Address.objects.create(
            **temporary_current_address_data
        )
        temporary_former_address = Address.objects.create(
            **temporary_former_address_data
        )
        contact_details = ContactDetail.objects.create(**contact_details_data)

        validated_data["permanent_current_address"] = permanent_current_address
        validated_data["permanent_former_address"] = permanent_former_address
        validated_data["temporary_current_address"] = temporary_current_address
        validated_data["temporary_former_address"] = temporary_former_address
        validated_data["contact_details"] = contact_details

        prd = PublicRepresentativeDetail.objects.create(**validated_data)
        return prd

    def update(self, instance, validated_data):
        permanent_current_address_data = validated_data.pop("permanent_current_address")
        permanent_former_address_data = validated_data.pop("permanent_former_address")
        temporary_current_address_data = validated_data.pop("temporary_current_address")
        temporary_former_address_data = validated_data.pop("temporary_former_address")
        contact_details_data = validated_data.pop("contact_details")

        if permanent_current_address_data:
            permanent_current_address_serializer = AddressSerializer(
                instance.permanent_current_address, data=permanent_current_address_data
            )
            if permanent_current_address_data["municipality"]:
                municipality = permanent_current_address_data.pop("municipality").id
                permanent_current_address_data["municipality"] = municipality

            if permanent_current_address_serializer.is_valid():
                permanent_current_address = permanent_current_address_serializer.save()
                validated_data["permanent_current_address"] = permanent_current_address

        if permanent_former_address_data:
            permanent_former_address_serializer = AddressSerializer(
                instance.permanent_former_address, data=permanent_former_address_data
            )
            if permanent_former_address_data["municipality"]:
                municipality = permanent_former_address_data.pop("municipality").id
                permanent_former_address_data["municipality"] = municipality

            if permanent_former_address_serializer.is_valid():
                permanent_former_address = permanent_former_address_serializer.save()
                validated_data["permanent_former_address"] = permanent_former_address

        if temporary_current_address_data:
            temporary_current_address_serializer = AddressSerializer(
                instance.temporary_current_addresss, data=temporary_current_address_data
            )
            if temporary_former_address_data["municipality"]:
                municipality = temporary_former_address_data.pop("municipality").id
                temporary_former_address_data["municipality"] = municipality

            if temporary_current_address_serializer.is_valid():
                temporary_current_address = temporary_current_address_serializer.save()
                validated_data["temporary_current_address"] = temporary_current_address

        if temporary_former_address_data:
            temporary_former_address_serializer = AddressSerializer(
                instance.temporary_former_address, data=temporary_former_address_data
            )
            if temporary_former_address_data["municipality"]:
                municipality = temporary_former_address_data.pop("municipality").id
                temporary_former_address_data["municipality"] = municipality

            if temporary_former_address_serializer.is_valid():
                temporary_former_address = temporary_former_address_serializer.save()
                validated_data["temporary_former_address"] = temporary_former_address

        if contact_details_data:
            contact_details_serializer = ContactDetailSerializer(
                instance.contact_details, data=contact_details_data
            )
            if contact_details_serializer.is_valid():
                contact_details = contact_details_serializer.save()
                validated_data["contact_details"] = contact_details
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tax_payer = instance.tax_payer
        religion = instance.religion
        language = instance.language
        country = instance.country
        nationality = instance.nationality

        representation["tax_payer"] = (
            self.tax_payer_data(tax_payer) if tax_payer else None
        )
        representation["religion"] = (
            self.get_common_data(religion) if religion else None
        )
        representation["language"] = (
            self.get_common_data(language) if language else None
        )
        representation["country"] = self.get_common_data(country) if country else None
        representation["nationality"] = (
            self.get_common_data(nationality) if nationality else None
        )
        return representation

    def get_common_data(self, data):
        return {"id": data.id, "name": data.name, "name_eng": data.name_eng}

    def tax_payer_data(self, data):
        return {
            "id": data.id,
            "tax_payer_no": data.tax_payer_no,
            "internal_source_no": data.internal_source_no,
            "tax_payer_name": data.tax_payer_name,
            "citizenship_no": data.citizenship_no,
        }
