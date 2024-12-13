"""
-- Created by Bikash Saud
--
-- Created on 2023-06-07
"""

from typing import Dict
from wsgiref import validate

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import exceptions, serializers

from base_model.base_serializers import (
    BaseSerializer,
    WriteableNestedModelBaseSerializer,
)
from base_model.models import (
    Address,
    CommonFieldsBase,
    ContactDetail,
    ContactPerson,
    DocumentType,
    Gender,
)
from base_model.serializers import (
    AddressSerializer,
    ContactDetailSerializer,
    ContactPersonSerializer,
)
from base_model.utils import get_relation_id
from employee.models import (
    Country,
    Language,
    Nationality,
    Position,
    PositionLevel,
    Religion,
    TaxPayer,
)
from plan_execution.models import UserCommitteeMonitoring
from project.models import FinancialYear

from .models import (
    BFI,
    AccountTitleManagement,
    BankAccount,
    BankType,
    BudgetSource,
    BudgetSubTitle,
    ChequeFormat,
    CollectPayment,
    ConstructionMaterialDescription,
    ConsumerCommittee,
    ConsumerCommitteeDocument,
    ConsumerCommitteeMember,
    Currency,
    ExecutiveAgency,
    MemberType,
    Module,
    MonitoringCommittee,
    MonitoringCommitteeDocument,
    MonitoringCommitteeMember,
    NewsPaper,
    Organization,
    OrganizationDocument,
    OrganizationMember,
    OrganizationType,
    PaymentMedium,
    PaymentMethod,
    ProjectStartDecision,
    SourceBearerEntity,
    SourceBearerEntityType,
    SourceReceipt,
    SubLedger,
    SubModule,
)


class CommonSerializer(serializers.ModelSerializer):
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

    def get_fields(self):
        fields = dict(super().get_fields())
        for field_name, field_class in fields.items():
            field_class.required = False
            field_class.allow_null = True
            field_class.allow_blank = True
        return fields


class PaymentMediumSerializer(CommonSerializer):
    class Meta:
        model = PaymentMedium
        fields = ("id", "code", "name", "name_eng", "status", "detail")
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }


class ChequeFormatSerializer(CommonSerializer):
    class Meta:
        model = ChequeFormat
        fields = ("id", "code", "name", "name_eng", "status", "detail")
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }


class BankTypeSerializer(CommonSerializer):
    class Meta:
        model = BankType
        fields = ("id", "code", "name", "name_eng", "status", "detail")
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }


class ModuleSerializer(CommonSerializer):
    class Meta:
        model = SubModule
        fields = ("id", "code", "name", "name_eng", "status", "detail", "remarks")
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
        }


class SubModuleSerializer(CommonSerializer):
    module = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = SubModule
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "status",
            "detail",
            "module",
            "remarks",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
            "module": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        module = instance.module
        representation["module"] = self.get_module(module) if module else None
        return representation

    @staticmethod
    def get_module(data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
            "code": data.code,
        }


class NewsPaperSerializer(CommonSerializer):
    class Meta:
        model = NewsPaper
        fields = "__all__"
        read_only_fields = ("id", "created_by")


class ProjectStartDecisionSerializer(CommonSerializer):
    class Meta:
        model = ProjectStartDecision
        fields = "__all__"
        read_only_fields = ("id", "created_by")


class ConstructionMaterialDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionMaterialDescription
        fields = "__all__"
        read_only_fields = ("id", "created_by")


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name", "name_eng", "status", "detail")
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }


class BFISerializer(serializers.ModelSerializer):
    bank_type = serializers.PrimaryKeyRelatedField(
        queryset=BankType.objects.all(), required=False, allow_null=True
    )
    cheque_format = serializers.PrimaryKeyRelatedField(
        queryset=ChequeFormat.objects.all(), required=False, allow_null=True
    )
    current_address = AddressSerializer(required=False, allow_null=True)
    former_address = AddressSerializer(required=False, allow_null=True)
    contact_detail = ContactDetailSerializer(required=False, allow_null=True)
    contact_person = ContactPersonSerializer(required=False, allow_null=True)

    class Meta:
        model = BFI
        fields = (
            "id",
            "code",
            "bank_type",
            "cheque_format",
            "full_name",
            "full_name_eng",
            "registration_no",
            "registration_date",
            "office",
            "detail",
            "current_address",
            "former_address",
            "contact_detail",
            "contact_person",
            "status",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "bank_type": {"required": False, "allow_null": True},
            "cheque_format": {"required": False, "allow_null": True},
            "full_name": {"required": False, "allow_null": True},
            "full_name_eng": {"required": False, "allow_null": True},
            "registration_no": {"required": False, "allow_null": True},
            "registration_date": {"required": False, "allow_null": True},
            "office": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
            "current_address": {"required": False, "allow_null": True},
            "former_address": {"required": False, "allow_null": True},
            "contact_detail": {"required": False, "allow_null": True},
            "contact_person": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        read_only_fields = ("id", "created_by")

    def create(self, validated_data):
        current_address_data = validated_data.pop("current_address")
        former_address_data = validated_data.pop("former_address")
        contact_detail_data = validated_data.pop("contact_detail")
        contact_person_data = validated_data.pop("contact_person")
        # bank_type = validated_data.pop("bank_type")
        # cheque_format = validated_data.pop("cheque_format")

        current_address = Address.objects.create(**current_address_data)
        former_address = Address.objects.create(**former_address_data)
        contact_detail = ContactDetail.objects.create(**contact_detail_data)
        contact_person = ContactPerson.objects.create(**contact_person_data)

        validated_data["current_address"] = current_address
        validated_data["former_address"] = former_address
        validated_data["contact_detail"] = contact_detail
        validated_data["contact_person"] = contact_person
        # validated_data['bank_type'] = bank_type.id if bank_type else None
        # validated_data['cheque_format'] = cheque_format.id if cheque_format else None
        bfi_detail = BFI.objects.create(**validated_data)
        return bfi_detail

    def update(self, instance, validated_data):
        current_address_data = validated_data.pop("current_address", None)
        former_address_data = validated_data.pop("former_address", None)
        contact_detail_data = validated_data.pop("contact_detail", None)
        contact_person_data = validated_data.pop("contact_person", None)

        if current_address_data.get("municipality") and (
            isinstance(current_address_data.get("municipality"), str)
            or isinstance(current_address_data.get("municipality"), int)
        ):
            current_address_data["municipality"] = current_address_data.get(
                "municipality"
            ).id

        if former_address_data.get("municipality") and (
            isinstance(former_address_data.get("municipality"), str)
            or isinstance(former_address_data.get("municipality"), int)
        ):
            former_address_data["municipality"] = former_address_data.get(
                "municipality"
            ).id

        if current_address_data:
            current_address_serializer = AddressSerializer(
                instance.current_address, data=current_address_data
            )
            if current_address_serializer.is_valid():
                current_address = current_address_serializer.save()
                validated_data["current_address"] = current_address

        if former_address_data:
            former_address_serializer = AddressSerializer(
                instance.former_address, data=former_address_data
            )
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        bank_type = (
            self.bank_type_data(instance.bank_type) if instance.bank_type else None
        )
        cheque_format = (
            self.cheque_format_data(instance.cheque_format)
            if instance.cheque_format
            else None
        )
        representation["cheque_format"] = cheque_format
        representation["bank_type"] = bank_type
        return representation

    def bank_type_data(self, obj):
        return BankTypeSerializer(obj.bank_type).data

    def cheque_format_data(self, obj):
        return ChequeFormatSerializer(obj.cheque_format).data


class BankAccountSerializer(serializers.ModelSerializer):
    currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(), allow_null=True, required=False
    )
    bank_name = serializers.PrimaryKeyRelatedField(
        queryset=BFI.objects.all(), allow_null=True, required=False
    )
    sub_module = serializers.PrimaryKeyRelatedField(
        queryset=SubModule.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = BankAccount
        fields = (
            "id",
            "account_no",
            "currency",
            "branch_code",
            "branch_name",
            "branch_name_eng",
            "bank_name",
            "sub_module",
            "status",
        )
        extra_kwargs = {
            "account_no": {"required": False, "allow_null": True},
            "currency": {"required": False, "allow_null": True},
            "branch_code": {"required": False, "allow_null": True},
            "branch_name": {"required": False, "allow_null": True},
            "branch_name_eng": {"required": False, "allow_null": True},
            "bank_name": {"required": False, "allow_null": True},
            "sub_module": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        currency_id = validated_data.pop("currency", None)
        bank_name_id = validated_data.pop("bank_name", None)
        sub_module_id = validated_data.pop("sub_module", None)

        bank_account = BankAccount.objects.create(**validated_data)
        if currency_id:
            bank_account.currency_id = currency_id
        if bank_name_id:
            bank_account.bank_name_id = bank_name_id
        if sub_module_id:
            bank_account.sub_module_id = sub_module_id
        bank_account.save()
        return bank_account


class BankAccountViewSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField(read_only=True)
    bank_name = serializers.SerializerMethodField(read_only=True)
    sub_module = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BankAccount
        fields = "__all__"

    def get_currency(self, obj):
        if obj.currency:
            return CurrencySerializer(obj.currency).data
        return None

    def get_bank_name(self, obj):
        if obj.bank_name:
            return BFISerializer(obj.bank_name).data
        return None

    def get_sub_module(self, obj):
        if obj.sub_module:
            return SubModuleSerializer(obj.sub_module).data
        return None


class OrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationType
        fields = ("id", "code", "name", "name_eng", "status", "detail")
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }


class OrganizationSerializer(WritableNestedModelSerializer):
    organization_type = OrganizationTypeSerializer(read_only=True)
    current_address = AddressSerializer()
    former_address = AddressSerializer()
    contact_detail = ContactDetailSerializer()
    contact_person = ContactPersonSerializer()

    class Meta:
        model = Organization
        fields = (
            "id",
            "code",
            "status",
            "organization_type",
            "is_loan",
            "full_name",
            "full_name_eng",
            "register_no",
            "register_date_bs",
            "register_date_eng",
            "office",
            "other_details",
            "pan_number",
            "current_address",
            "former_address",
            "contact_detail",
            "contact_person",
            "remarks",
            "display_order",
        )

        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "organization_type": {"required": False, "allow_null": True},
            "is_loan": {"required": False, "allow_null": True},
            "full_name": {"required": False, "allow_null": True},
            "full_name_eng": {"required": False, "allow_null": True},
            "register_no": {"required": False, "allow_null": True},
            "register_date_bs": {"required": False, "allow_null": True},
            "register_date_eng": {"required": False, "allow_null": True},
            "office": {"required": False, "allow_null": True},
            "other_details": {"required": False, "allow_null": True},
            "pan_number": {"required": False, "allow_null": True},
            "current_address": {"required": False, "allow_null": True},
            "former_address": {"required": False, "allow_null": True},
            "contact_detail": {"required": False, "allow_null": True},
            "contact_person": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "display_order": {"required": False, "allow_null": True},
        }
        read_only_fields = ("id", "created_by")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        organization_type = instance.organization_type
        contact_person = instance.contact_person
        representation["organization_type"] = (
            self.get_organization_type(organization_type) if organization_type else None
        )
        representation["contact_person"] = (
            self.get_contact_person(contact_person) if contact_person else None
        )
        return representation

    def get_organization_type(self, data):
        return {
            "id": data.id,
            "code": data.code,
            "name": data.name,
        }

    def get_contact_person(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
            "position": data.position,
            "phone_number": data.phone_number,
            "mobile_number": data.mobile_number,
            "email": data.email,
        }


class OrganizationMemberSerializer(serializers.ModelSerializer):
    organization_id = OrganizationSerializer()

    class Meta:
        model = OrganizationMember
        fields = (
            "full_name",
            "full_name_eng",
            "phone_number",
            "email",
            "position_start_date",
            "position_start_date_eng",
            "position_end_date",
            "position_end_date_eng",
            "remarks",
            "status",
            "address",
        )
        extra_kwargs = {
            "full_name": {"required": False, "allow_null": True},
            "full_name_eng": {"required": False, "allow_null": True},
            "phone_number": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
            "position_start_date": {"required": False, "allow_null": True},
            "position_start_date_eng": {"required": False, "allow_null": True},
            "position_end_date": {"required": False, "allow_null": True},
            "position_end_date_eng": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
        }


class OrganizationMemberSerializer(serializers.ModelSerializer):
    organization_member_id = OrganizationSerializer()

    class Meta:
        model = OrganizationMember
        fields = ("organization_member_id",)
        extra_kwargs = {
            "organization_member_id": {"required": False, "allow_null": True},
        }


class MemberTypeSerializer(CommonSerializer):
    class Meta:
        model = MemberType
        fields = CommonSerializer.Meta.fields


class MonitoringCommitteeDocumentSerializer(serializers.ModelSerializer):
    document_type = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(), required=False, allow_null=True
    )
    monitoring_committee = serializers.PrimaryKeyRelatedField(
        queryset=MonitoringCommittee.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = MonitoringCommitteeDocument
        fields = (
            "id",
            "document_type",
            "document_file",
            "document_name",
            "document_size",
            "monitoring_committee",
            "status",
        )


class MonitoringCommitteeMemberSerializer(WriteableNestedModelBaseSerializer):
    tax_payer = serializers.PrimaryKeyRelatedField(
        queryset=TaxPayer.objects.all(), required=False, allow_null=True
    )
    member_type = serializers.PrimaryKeyRelatedField(
        queryset=MemberType.objects.all(), required=False, allow_null=True
    )
    permanent_current_address = AddressSerializer(required=False, allow_null=True)
    permanent_former_address = AddressSerializer(required=False, allow_null=True)
    temporary_current_address = AddressSerializer(required=False, allow_null=True)
    temporary_former_address = AddressSerializer(required=False, allow_null=True)
    contact_details = ContactDetailSerializer(required=False, allow_null=True)
    position = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), required=False, allow_null=True
    )
    position_level = serializers.PrimaryKeyRelatedField(
        queryset=PositionLevel.objects.all(), required=False, allow_null=True
    )
    monitoring_committee = serializers.PrimaryKeyRelatedField(
        queryset=MonitoringCommittee.objects.all(), required=False, allow_null=True
    )
    gender = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.all(), required=False, allow_null=True
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
    user_committee_monitoring = serializers.PrimaryKeyRelatedField(
        queryset=UserCommitteeMonitoring.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = MonitoringCommitteeMember
        fields = (
            "id",
            "ethnicity",
            "member_type",
            "is_monitoring_team_member",
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
            "gender",
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
            "voter_start_district",
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
            "monitoring_committee",
            "status",
            "user_committee_monitoring",
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        tax_payer = instance.tax_payer
        rep["tax_payer"] = self.get_common_data(tax_payer) if tax_payer else None
        member_type = instance.member_type
        rep["member_type"] = self.get_common_data(member_type) if member_type else None
        position = instance.position
        rep["position"] = self.get_common_data(position) if position else None
        position_level = instance.position_level
        rep["position_level"] = (
            self.get_common_data(position_level) if position_level else None
        )
        gender = instance.gender
        rep["gender"] = self.get_common_data(gender) if gender else None
        religion = instance.religion
        rep["religion"] = self.get_common_data(religion) if religion else None
        language = instance.language
        rep["language"] = self.get_common_data(language) if language else None
        country = instance.country
        rep["country"] = self.get_common_data(country) if country else None
        nationality = instance.nationality
        rep["nationality"] = self.get_common_data(nationality) if nationality else None
        return rep

    @staticmethod
    def correct_data(monitoring_committee_member_data: dict) -> dict:
        if monitoring_committee_member_data:
            monitoring_committee_member_data["member_type"] = get_relation_id(
                monitoring_committee_member_data, "member_type"
            )
            monitoring_committee_member_data["tax_payer"] = get_relation_id(
                monitoring_committee_member_data, "tax_payer"
            )
            monitoring_committee_member_data["member_type"] = get_relation_id(
                monitoring_committee_member_data, "member_type"
            )
            monitoring_committee_member_data["position"] = get_relation_id(
                monitoring_committee_member_data, "position"
            )
            monitoring_committee_member_data["position_level"] = get_relation_id(
                monitoring_committee_member_data, "position_level"
            )
            monitoring_committee_member_data["monitoring_committee"] = get_relation_id(
                monitoring_committee_member_data, "monitoring_committee"
            )
            monitoring_committee_member_data["gender"] = get_relation_id(
                monitoring_committee_member_data, "gender"
            )
            monitoring_committee_member_data["religion"] = get_relation_id(
                monitoring_committee_member_data, "religion"
            )
            monitoring_committee_member_data["language"] = get_relation_id(
                monitoring_committee_member_data, "language"
            )
            monitoring_committee_member_data["country"] = get_relation_id(
                monitoring_committee_member_data, "country"
            )
            monitoring_committee_member_data["nationality"] = get_relation_id(
                monitoring_committee_member_data, "nationality"
            )
            monitoring_committee_member_data["user_committee_monitoring"] = (
                get_relation_id(
                    monitoring_committee_member_data, "user_committee_monitoring"
                )
            )
        return monitoring_committee_member_data

    def to_internal_value(self, data):
        updated_data = self.correct_data(data)
        return super().to_internal_value(updated_data)


class ConsumerCommitteeDocumentSerializer(serializers.ModelSerializer):
    document_type = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(), required=False, allow_null=True
    )
    consumer_committee = serializers.PrimaryKeyRelatedField(
        queryset=ConsumerCommittee.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ConsumerCommitteeDocument
        fields = (
            "id",
            "document_type",
            "document_file",
            "document_name",
            "document_size",
            "consumer_committee",
            "status",
        )
        extra_kwargs = {
            "document_type": {"required": False, "allow_null": True},
            "document_name": {"required": False, "allow_null": True},
            "document_size": {"required": False, "allow_null": True},
            "consumer_committee": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class ConsumerCommitteeMemberSerializer(WriteableNestedModelBaseSerializer):
    tax_payer = serializers.PrimaryKeyRelatedField(
        queryset=TaxPayer.objects.all(), required=False, allow_null=True
    )
    member_type = serializers.PrimaryKeyRelatedField(
        queryset=MemberType.objects.all(), required=False, allow_null=True
    )
    permanent_current_address = AddressSerializer(required=False, allow_null=True)
    permanent_former_address = AddressSerializer(required=False, allow_null=True)
    temporary_current_address = AddressSerializer(required=False, allow_null=True)
    temporary_former_address = AddressSerializer(required=False, allow_null=True)
    contact_details = ContactDetailSerializer(required=False, allow_null=True)
    position = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), required=False, allow_null=True
    )
    position_level = serializers.PrimaryKeyRelatedField(
        queryset=PositionLevel.objects.all(), required=False, allow_null=True
    )
    consumer_committee = serializers.PrimaryKeyRelatedField(
        queryset=ConsumerCommittee.objects.all(), required=False, allow_null=True
    )
    gender = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.all(), required=False, allow_null=True
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

    class Meta:
        model = ConsumerCommitteeMember
        fields = (
            "id",
            "ethnicity",
            "member_type",
            "is_monitoring_team_member",
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
            "gender",
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
            "voter_start_district",
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
            "consumer_committee",
            "status",
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        tax_payer = instance.tax_payer
        rep["tax_payer"] = self.get_common_data(tax_payer) if tax_payer else None
        member_type = instance.member_type
        rep["member_type"] = self.get_common_data(member_type) if member_type else None
        position = instance.position
        rep["position"] = self.get_common_data(position) if position else None
        position_level = instance.position_level
        rep["position_level"] = (
            self.get_common_data(position_level) if position_level else None
        )
        gender = instance.gender
        rep["gender"] = self.get_common_data(gender) if gender else None
        religion = instance.religion
        rep["religion"] = self.get_common_data(religion) if religion else None
        language = instance.language
        rep["language"] = self.get_common_data(language) if language else None
        country = instance.country
        rep["country"] = self.get_common_data(country) if country else None
        nationality = instance.nationality
        rep["nationality"] = self.get_common_data(nationality) if nationality else None
        return rep


class MonitoringCommitteeSerializer(WriteableNestedModelBaseSerializer):
    contact_person = ContactPersonSerializer()
    current_address = AddressSerializer()
    former_address = AddressSerializer()
    contact_detail = ContactDetailSerializer()
    bank = serializers.PrimaryKeyRelatedField(
        queryset=BFI.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = MonitoringCommittee
        fields = (
            "id",
            "contact_person",
            "current_address",
            "former_address",
            "contact_detail",
            "code",
            "status",
            "ward",
            "full_name",
            "date",
            "date_eng",
            "bank",
            "bank_acc_no",
            "bank_branch",
            "full_name_eng",
            "consumer_comittee_type",
            "present_quantity",
            "member_quantity",
            "witness",
            "registration_no",
            "registration_date",
            "registration_date_eng",
            "office",
            "detail",
            "remarks",
            "kramagat",
        )


class ConsumerCommitteeSerializer(WriteableNestedModelBaseSerializer):
    contact_person = ContactPersonSerializer()
    current_address = AddressSerializer()
    former_address = AddressSerializer()
    contact_detail = ContactDetailSerializer()
    bank = serializers.PrimaryKeyRelatedField(
        queryset=BFI.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ConsumerCommittee
        fields = (
            "id",
            "contact_person",
            "current_address",
            "former_address",
            "contact_detail",
            "code",
            "status",
            "ward",
            "full_name",
            "date",
            "date_eng",
            "bank",
            "bank_acc_no",
            "bank_branch",
            "full_name_eng",
            "consumer_comittee_type",
            "present_quantity",
            "member_quantity",
            "witness",
            "registration_no",
            "registration_date",
            "registration_date_eng",
            "office",
            "detail",
            "remarks",
            "kramagat",
        )


class ExecutiveAgencySerializer(serializers.ModelSerializer):
    contact_person = ContactPersonSerializer()
    current_address = AddressSerializer()
    former_address = AddressSerializer()
    contact_detail = ContactDetailSerializer()
    bank = serializers.PrimaryKeyRelatedField(
        queryset=BFI.objects.all(), required=False, allow_null=True
    )
    consumer_comittee_type = serializers.PrimaryKeyRelatedField(
        queryset=MemberType.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ExecutiveAgency
        fields = (
            "id",
            "contact_person",
            "current_address",
            "former_address",
            "contact_detail",
            "code",
            "status",
            "ward",
            "full_name",
            "date",
            "date_eng",
            "bank",
            "bank_acc_no",
            "bank_branch",
            "full_name_eng",
            "consumer_comittee_type",
            "present_quantity",
            "member_quantity",
            "witness",
            "registration_no",
            "registration_date",
            "registration_date_eng",
            "office",
            "detail",
            "remarks",
            "kramagat",
        )
        extra_kwargs = {
            "contact_person": {"required": False, "allow_null": True},
            "current_address": {"required": False, "allow_null": True},
            "former_address": {"required": False, "allow_null": True},
            "contact_detail": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "ward": {"required": False, "allow_null": True},
            "full_name": {"required": False, "allow_null": True},
            "date": {"required": False, "allow_null": True},
            "date_eng": {"required": False, "allow_null": True},
            "bank": {"required": False, "allow_null": True},
            "bank_acc_no": {"required": False, "allow_null": True},
            "bank_branch": {"required": False, "allow_null": True},
            "full_name_eng": {"required": False, "allow_null": True},
            "consumer_comittee_type": {"required": False, "allow_null": True},
            "present_quantity": {"required": False, "allow_null": True},
            "member_quantity": {"required": False, "allow_null": True},
            "witness": {"required": False, "allow_null": True},
            "registration_no": {"required": False, "allow_null": True},
            "registration_date": {"required": False, "allow_null": True},
            "registration_date_eng": {"required": False, "allow_null": True},
            "office": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "kramagat": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        contact_person_data = validated_data.pop("contact_person")
        current_address_data = validated_data.pop("current_address")
        former_address_data = validated_data.pop("former_address")
        contact_detail_data = validated_data.pop("contact_detail")

        contact_person_serializer = ContactPersonSerializer(data=contact_person_data)
        current_address_serializer = AddressSerializer(data=current_address_data)
        former_address_serializer = AddressSerializer(data=former_address_data)
        contact_detail_serializer = ContactDetailSerializer(data=contact_detail_data)

        if not contact_person_serializer.is_valid():
            raise exceptions.ValidationError(contact_person_serializer.errors)
        if not current_address_serializer.is_valid():
            raise exceptions.ValidationError(current_address_serializer.errors)
        if not former_address_serializer.is_valid():
            raise exceptions.ValidationError(former_address_serializer.errors)
        if not contact_detail_serializer.is_valid():
            raise exceptions.ValidationError(contact_detail_serializer.errors)

        contact_person = contact_person_serializer.save()
        current_address = current_address_serializer.save()
        former_address = former_address_serializer.save()
        contact_detail = contact_detail_serializer.save()

        validated_data["contact_person"] = contact_person
        validated_data["current_address"] = current_address
        validated_data["former_address"] = former_address
        validated_data["contact_detail"] = contact_detail

        return super().create(validated_data)


class BudgetSubTitleSerializer(CommonSerializer):
    class Meta:
        model = BudgetSubTitle
        fields = CommonSerializer.Meta.fields


class PaymentMethodSerializer(CommonSerializer):
    class Meta:
        model = PaymentMethod
        fields = CommonSerializer.Meta.fields


class SourceReceiptSerializer(CommonSerializer):
    class Meta:
        model = SourceReceipt
        fields = CommonSerializer.Meta.fields


class CollectPaymentSerializer(CommonSerializer):
    class Meta:
        model = CollectPayment
        fields = CommonSerializer.Meta.fields


class SubLedgerSerializer(CommonSerializer):
    class Meta:
        model = SubLedger
        fields = CommonSerializer.Meta.fields + ("karmagat",)


class ATMSerializer(CommonSerializer):
    module = serializers.PrimaryKeyRelatedField(
        queryset=SubModule.objects.all(), required=False, allow_null=True
    )
    sub_module = serializers.PrimaryKeyRelatedField(
        queryset=SubModule.objects.all(), required=False, allow_null=True
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=AccountTitleManagement.objects.all(), required=False, allow_null=True
    )
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False, allow_null=True
    )
    has_children = serializers.BooleanField(read_only=True)

    class Meta:
        model = AccountTitleManagement
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "optional_code",
            "display_name",
            "display_name_eng",
            "is_budgeted",
            "sapati",
            "transfer_account",
            "fund_account",
            "base_account",
            "is_transactable",
            "current_capital",
            "current_ratio",
            "capital_ratio",
            "detail",
            "status",
            "parent",
            "module",
            "sub_module",
            "financial_year",
            "has_children",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "optional_code": {"required": False, "allow_null": True},
            "display_name": {"required": False, "allow_null": True},
            "display_name_eng": {"required": False, "allow_null": True},
            "is_budgeted": {"required": False, "allow_null": True},
            "sapati": {"required": False, "allow_null": True},
            "transfer_account": {"required": False, "allow_null": True},
            "fund_account": {"required": False, "allow_null": True},
            "base_account": {"required": False, "allow_null": True},
            "is_transactable": {"required": False, "allow_null": True},
            "current_capital": {"required": False, "allow_null": True},
            "current_ratio": {"required": False, "allow_null": True},
            "capital_ratio": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "parent": {"required": False, "allow_null": True},
            "module": {"required": False, "allow_null": True},
            "sub_module": {"required": False, "allow_null": True},
            "financial_year": {"required": False, "allow_null": True},
            "has_children": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["parent"] = (
            self.get_common_data(instance.parent) if instance.parent else None
        )
        representation["module"] = (
            self.get_common_data(instance.module) if instance.module else None
        )
        representation["sub_module"] = (
            self.get_common_data(instance.sub_module) if instance.sub_module else None
        )
        representation["financial_year"] = (
            self.get_fy(instance.financial_year) if instance.financial_year else None
        )

        return representation

    def get_fy(self, data):
        return {
            "id": data.id,
            "start_year": data.start_year,
            "end_year": data.end_year,
            "fy": data.fy,
        }

    def get_common_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
        }

    def update(self, instance, validated_data):
        code = validated_data.pop("code", None)
        return super().update(instance, validated_data)


class BudgetSourceSerializer(CommonSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=BudgetSource.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = BudgetSource
        fields = (
            "id",
            "code",
            "parent",
            "name",
            "name_eng",
            "phone_number",
            "email",
            "country",
            "address",
            "status",
            "detail",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "parent": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "phone_number": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
            "country": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        parent = instance.parent
        representation["parent"] = self.get_common_data(parent) if parent else None
        return representation

    def get_common_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
        }


class SBETypeSerializer(CommonSerializer):
    class Meta:
        model = SourceBearerEntityType
        fields = CommonSerializer.Meta.fields


class DocumentTypeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    name_eng = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    detail = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = DocumentType
        fields = (
            "id",
            "document_type",
            "code",
            "name",
            "name_eng",
            "detail",
            "status",
        )
        extra_kwargs = {
            "document_type": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class SBESerializer(CommonSerializer):
    bearer_type = serializers.PrimaryKeyRelatedField(
        queryset=SourceBearerEntityType.objects.all(), required=False, allow_null=True
    )
    organization_name = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = SourceBearerEntity
        fields = CommonSerializer.Meta.fields + (
            "bearer_type",
            "organization_name",
            "karmagat",
        )
        extra_kwargs = {
            "bearer_type": {"required": False, "allow_null": True},
            "organization_name": {"required": False, "allow_null": True},
            "karmagat": {"required": False, "allow_null": True},
        }

    def validate(self, attrs):
        return super().validate(attrs, validate_name=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        bearer_type = instance.bearer_type
        organization_name = instance.organization_name
        representation["bearer_type"] = (
            self.get_common_data(bearer_type) if bearer_type else None
        )
        representation["organization_name"] = (
            self.get_sbe_data(organization_name) if organization_name else None
        )
        return representation

    def get_common_data(self, data):
        return {"id": data.id, "name": data.name, "name_eng": str(data.name_eng)}

    def get_sbe_data(self, data):
        return {
            "id": data.id,
            "full_name": data.full_name,
            "full_name_eng": data.full_name_eng,
            "register_no": data.register_no,
        }
