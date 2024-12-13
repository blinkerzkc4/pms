"""
-- Created by Bikash Saud
--
-- Created on 2023-06-18
"""
from rest_framework import serializers

from base_model.models import Address, DocumentType
from base_model.serializers import AddressSerializer
from base_model.base_serializers import CommonSerializer
from budget_process.models import ApproveProcess
from budget_process.serializers import ApproveProcessSerializer
from employee.models import Employee
from employee.serializers import EmployeeSerializer
from formulate_plan.models import (
    BudgetAssurance,
    ProjectAddress,
    ProjectDocument,
    ProjectWorkType,
    WorkClass,
    WorkProject,
)
from project.models import FinancialYear, Unit
from project_planning.basic_description_serializers import ExpanseTypeSerializer
from project_planning.models import (
    ConsumerCommittee,
    ExpanseType,
    PriorityType,
    ProjectProposedType,
    Road,
)
from project_report.models import ReportType
from utils import report_utils


class WorkClassSerializer(CommonSerializer):
    class Meta:
        model = WorkClass
        fields = (
            "id",
            "name",
            "name_eng",
            "code",
            "status",
        )


class ProjectWorkTypeSerializer(CommonSerializer):
    class_of_work = serializers.PrimaryKeyRelatedField(
        queryset=WorkClass.objects.all(), required=False
    )

    class Meta:
        model = ProjectWorkType
        fields = (
            "id",
            "name",
            "name_eng",
            "code",
            "detail",
            "status",
            "class_of_work",
            "priority_class",
            "overall_priority",
            "max_budget",
            "min_budget",
            "kramagat",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "class_of_work": {"required": False, "allow_null": True},
            "priority_class": {"required": False, "allow_null": True},
            "overall_priority": {"required": False, "allow_null": True},
            "max_budget": {"required": False, "allow_null": True},
            "min_budget": {"required": False, "allow_null": True},
            "kramagat": {"required": False, "allow_null": True},
        }
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        class_of_work = instance.class_of_work
        if class_of_work:
            representation["class_of_work"] = {
                "id": class_of_work.id,
                "name": class_of_work.name,
                "name_eng": str(class_of_work.name_eng),
                "code": str(class_of_work.code),
            }
        else:
            representation["class_of_work"] = None
        return representation


class BudgetAssuranceSerializer(serializers.ModelSerializer):
    expense_title_name = serializers.PrimaryKeyRelatedField(
        queryset=ExpanseType.objects.all(), required=False, allow_null=True
    )
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = BudgetAssurance
        fields = (
            "id",
            "amount",
            "internal_source",
            "nepal_gov_source",
            "province_source",
            "local_level_source",
            "loan_source",
            "public_participation_source",
            "expense_title_no",
            "expense_title_name",
            "program_activity_outcome",
            "past_fiscal_year_outcome",
            "past_fiscal_year_expense",
            "current_fy_outcome",
            "current_fy_budget",
            "first_quarter_outcome",
            "first_quarter_budget",
            "second_quarter_outcome",
            "second_quarter_budget",
            "third_quarter_outcome",
            "third_quarter_budget",
            "approved_by",
            "approved_date",
            "approved_date_eng",
            "status",
        )
        extra_kwargs = {
            "amount": {"required": False, "allow_null": True},
            "internal_source": {"required": False, "allow_null": True},
            "nepal_gov_source": {"required": False, "allow_null": True},
            "province_source": {"required": False, "allow_null": True},
            "local_level_source": {"required": False, "allow_null": True},
            "loan_source": {"required": False, "allow_null": True},
            "public_participation_source": {"required": False, "allow_null": True},
            "expense_title_no": {"required": False, "allow_null": True},
            "expense_title_name": {"required": False, "allow_null": True},
            "program_activity_outcome": {"required": False, "allow_null": True},
            "past_fiscal_year_outcome": {"required": False, "allow_null": True},
            "past_fiscal_year_expense": {"required": False, "allow_null": True},
            "current_fy_outcome": {"required": False, "allow_null": True},
            "current_fy_budget": {"required": False, "allow_null": True},
            "first_quarter_outcome": {"required": False, "allow_null": True},
            "first_quarter_budget": {"required": False, "allow_null": True},
            "second_quarter_outcome": {"required": False, "allow_null": True},
            "second_quarter_budget": {"required": False, "allow_null": True},
            "third_quarter_outcome": {"required": False, "allow_null": True},
            "third_quarter_budget": {"required": False, "allow_null": True},
            "approved_by": {"required": False, "allow_null": True},
            "approved_date": {"required": False, "allow_null": True},
            "approved_date_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        # read_only_fields = ("id",)


class WorkProjectSerializer(CommonSerializer):
    work_type = serializers.PrimaryKeyRelatedField(
        queryset=ProjectWorkType.objects.all(), required=False, allow_null=True
    )
    work_class = serializers.PrimaryKeyRelatedField(
        queryset=WorkClass.objects.all(), required=False, allow_null=True
    )
    proposed_type = serializers.PrimaryKeyRelatedField(
        queryset=ProjectProposedType.objects.all(), required=False, allow_null=True
    )
    user_committee = serializers.PrimaryKeyRelatedField(
        queryset=ConsumerCommittee.objects.all(), required=False, allow_null=True
    )
    proposed_financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False, allow_null=True
    )
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False, allow_null=True
    )
    proposed_unit_type = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(), required=False, allow_null=True
    )
    project_prioritization = serializers.PrimaryKeyRelatedField(
        queryset=PriorityType.objects.all(), required=False, allow_null=True
    )
    priority_approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    project_approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    address = AddressSerializer(required=False, allow_null=True)
    approve = ApproveProcessSerializer(required=False, allow_null=True)
    budget_assurance = BudgetAssuranceSerializer(required=False, allow_null=True)

    class Meta:
        model = WorkProject
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "status",
            "work_type",
            "work_class",
            "proposed_type",
            "user_committee",
            "ward",
            "proposed_financial_year",
            "financial_year",
            "proposed_unit_type",
            "proposed_project_outcome",
            "address",
            "project_level",
            "proposed_date",
            "proposed_date_eng",
            "estimated_start_date",
            "estimated_start_date_eng",
            "estimated_end_date",
            "estimated_end_date_eng",
            "estimated_amount",
            "internal_source",
            "nepal_gov",
            "province_gov",
            "local_level_gov",
            "loan",
            "public_participation",
            "benefited_households",
            "benefited_population",
            "achievement",
            "approve",
            "is_prioritized",
            "project_prioritization",
            "priority_approved_by",
            "priority_approved_date",
            "priority_approved_date_eng",
            "budget_assurance",
            "project_approved_date",
            "project_approved_date_eng",
            "project_approved_by",
            "is_approved",
            "approved_date",
            "approved_date_eng",
            "remarks",
            "kramagat",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "work_type": {"required": False, "allow_null": True},
            "work_class": {"required": False, "allow_null": True},
            "proposed_type": {"required": False, "allow_null": True},
            "user_committee": {"required": False, "allow_null": True},
            "ward": {"required": False, "allow_null": True},
            "proposed_financial_year": {"required": False, "allow_null": True},
            "financial_year": {"required": False, "allow_null": True},
            "proposed_unit_type": {"required": False, "allow_null": True},
            "proposed_project_outcome": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
            "project_level": {"required": False, "allow_null": True},
            "proposed_date": {"required": False, "allow_null": True},
            "proposed_date_eng": {"required": False, "allow_null": True},
            "estimated_start_date": {"required": False, "allow_null": True},
            "estimated_start_date_eng": {"required": False, "allow_null": True},
            "estimated_end_date": {"required": False, "allow_null": True},
            "estimated_end_date_eng": {"required": False, "allow_null": True},
            "estimated_amount": {"required": False, "allow_null": True},
            "internal_source": {"required": False, "allow_null": True},
            "nepal_gov": {"required": False, "allow_null": True},
            "province_gov": {"required": False, "allow_null": True},
            "local_level_gov": {"required": False, "allow_null": True},
            "loan": {"required": False, "allow_null": True},
            "public_participation": {"required": False, "allow_null": True},
            "benefited_households": {"required": False, "allow_null": True},
            "benefited_population": {"required": False, "allow_null": True},
            "achievement": {"required": False, "allow_null": True},
            "approve": {"required": False, "allow_null": True},
            "is_prioritized": {"required": False, "allow_null": True},
            "project_prioritization": {"required": False, "allow_null": True},
            "priority_approved_by": {"required": False, "allow_null": True},
            "priority_approved_date": {"required": False, "allow_null": True},
            "priority_approved_date_eng": {"required": False, "allow_null": True},
            "budget_assurance": {"required": False, "allow_null": True},
            "project_approved_date": {"required": False, "allow_null": True},
            "project_approved_date_eng": {"required": False, "allow_null": True},
            "project_approved_by": {"required": False, "allow_null": True},
            "is_approved": {"required": False, "allow_null": True},
            "approved_date": {"required": False, "allow_null": True},
            "approved_date_eng": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "kramagat": {"required": False, "allow_null": True},
        }
    def create(self, validated_data):
        approval_process_data = validated_data.pop("approve", None)
        if approval_process_data:
            approve = ApproveProcess.objects.create(**approval_process_data)
            validated_data["approve"] = approve

        address_data = validated_data.pop("address", None)
        if address_data:
            address = Address.objects.create(**address_data)
            validated_data["address"] = address

        budget_assurance_data = validated_data.pop("budget_assurance", None)
        if budget_assurance_data:
            budget_assurance = BudgetAssurance.objects.create(**budget_assurance_data)
            validated_data["budget_assurance"] = budget_assurance
        work_project = WorkProject.objects.create(**validated_data)
        return work_project

    def update(self, instance, validated_data):
        approve_data = validated_data.pop("approve", None)
        address_data = validated_data.pop("address", None)
        budget_assurance_data = validated_data.pop("budget_assurance", None)
        print(approve_data, address_data, budget_assurance_data, 99999999999)
        if address_data:
            address_serializer = AddressSerializer(instance.address, data=address_data)
            if address_data["municipality"]:
                municipality = address_data.pop("municipality").id
                address_data["municipality"] = municipality
            if address_serializer.is_valid():
                address = address_serializer.save()
                validated_data["address"] = address

        if approve_data:
            approve_serializer = AddressSerializer(instance.approve, data=approve_data)
            if approve_serializer.is_valid():
                approve = approve_serializer.save()
                validated_data["approve"] = approve
        if budget_assurance_data:
            budget_assurance_serializer = BudgetAssuranceSerializer(
                instance.budget_assurance, data=budget_assurance_data
            )
            expense_type_data = budget_assurance_data.pop("expense_title_name")
            approved_by = budget_assurance_data.pop("approved_by")
            budget_assurance_data.expense_title_name = expense_type_data.id
            budget_assurance_data.approved_by = approved_by.id
            if budget_assurance_serializer.is_valid():
                budget_assurance = budget_assurance_serializer.save()
                validated_data["budget_assurance"] = budget_assurance
            else:
                errors = budget_assurance_serializer.errors
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        work_type = instance.work_type
        project_level = instance.project_level
        proposed_type = instance.proposed_type
        work_class = instance.work_class
        user_committee = instance.user_committee
        proposed_financial_year = instance.proposed_financial_year
        financial_year = instance.financial_year
        proposed_unit_type = instance.proposed_unit_type
        project_prioritization = instance.project_prioritization
        priority_approved_by = instance.priority_approved_by
        project_approved_by = instance.project_approved_by

        representation["work_type"] = (
            self.get_common_data(work_type) if work_type else None
        )
        representation["project_level"] = (
            self.get_common_data(project_level) if project_level else None
        )
        representation["proposed_type"] = (
            self.get_common_data(proposed_type) if proposed_type else None
        )
        representation["work_class"] = (
            self.get_common_data(work_class) if work_class else None
        )
        representation["user_committee"] = (
            self.get_user_committee(user_committee) if user_committee else None
        )
        representation["financial_year"] = (
            self.get_fiscal_year(financial_year) if financial_year else None
        )
        representation["proposed_financial_year"] = (
            self.get_fiscal_year(proposed_financial_year)
            if proposed_financial_year
            else None
        )
        representation["proposed_unit_type"] = (
            self.get_unit(proposed_unit_type) if proposed_unit_type else None
        )
        representation["project_prioritization"] = (
            self.get_common_data(project_prioritization)
            if project_prioritization
            else None
        )
        representation["priority_approved_by"] = (
            self.get_employee(priority_approved_by) if priority_approved_by else None
        )
        representation["project_approved_by"] = (
            self.get_employee(project_approved_by) if project_approved_by else None
        )

        return representation

    def get_common_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": str(data.name_eng),
            "code": str(data.code),
        }

    def get_user_committee(self, data):
        return {
            "id": data.id,
            "code": data.code,
            "full_name": str(data.full_name),
            "full_name_eng": str(data.full_name_eng),
            "registration_no": str(data.registration_no),
        }

    def get_fiscal_year(self, data):
        return {
            "id": data.id,
            "start_year": data.start_year,
            "end_year": data.end_year,
            "fy": data.fy,
        }

    def get_unit(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": str(data.name_eng),
        }

    def get_employee(self, employee):
        return {
            "id": employee.id,
            "name": employee.first_name.join(employee.last_name),
            "dob": employee.dob,
            "phone_number": employee.phone_number,
        }


class ProjectAddressSerializer(AddressSerializer):
    road_name = serializers.PrimaryKeyRelatedField(
        queryset=Road.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectAddress
        fields = AddressSerializer.Meta.fields + ("village_name",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        road_name = instance.road_name
        representation["road_name"] = (
            self.get_road_name(road_name) if road_name else None
        )
        return representation

    def get_road_name(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": str(data.name_eng),
        }


class ProjectDocumentSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=WorkProject.objects.all())
    document_type = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all()
    )
    report_type = serializers.SlugRelatedField(
        queryset=ReportType.objects.all(), slug_field="code", required=False
    )

    class Meta:
        model = ProjectDocument
        fields = (
            "id",
            "project",
            "document_type",
            "document_file",
            "status",
            "report_type",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        document_type = instance.document_type
        report_type = instance.report_type
        representation["project"] = self.get_project(project) if project else None
        representation["document_type"] = (
            self.get_document_type(document_type) if document_type else None
        )
        representation["report_type"] = (
            self.get_report_type(report_type) if report_type else None
        )
        return representation

    def get_report_type(self, data):
        return {
            "id": data.id,
            "code": data.code,
            "name": data.name,
            "name_eng": data.name_eng,
        }

    def get_document_type(self, data):
        return {"id": data.id, "document_type": data.document_type}

    def get_project(self, data):
        return {"id": data.id, "name": data.name, "name_eng": data.name_eng}
