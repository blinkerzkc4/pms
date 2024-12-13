"""
-- Created by Bikash Saud
--
-- Created on 2023-06-17
"""

from rest_framework import serializers

from budget_process.models import (
    AccountTitleManagement,
    ApproveProcess,
    BudgetAmmendment,
    BudgetExpenseManagement,
    BudgetManagement,
    BudgetTransfer,
    EstimateFinancialArrangements,
    ExpenseBudgetRangeDetermine,
    IncomeBudgetRangeDetermine,
    IncomeExpenseDetermine,
    Source,
)
from employee.models import Employee
from employee.serializers import CommonSerializer, EmployeeSerializer
from project.models import FinancialYear
from project.serializers import FinancialYearSerializer
from project_planning.models import BudgetSource, SubjectArea, SubModule


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            "internal_source",
            "nepal_gov",
            "province_gov",
            "local_gov",
            "loan",
            "public_participation",
            "status",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "internal_source": {"required": False, "allow_null": True},
            "nepal_gov": {"required": False, "allow_null": True},
            "province_gov": {"required": False, "allow_null": True},
            "local_gov": {"required": False, "allow_null": True},
            "loan": {"required": False, "allow_null": True},
            "public_participation": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

class ApproveProcessSerializer(serializers.ModelSerializer):
    # prepared_by = EmployeeSerializer(read_only=True)
    # verified_by = EmployeeSerializer(read_only=True)
    # approved_by = EmployeeSerializer(read_only=True)

    class Meta:
        model = ApproveProcess
        fields = (
            "prepared_by",
            "is_prepared",
            "prepared_date",
            "prepared_date_eng",
            "verified_by",
            "is_verified",
            "verified_date",
            "verified_date_eng",
            "approved_by",
            "is_approved",
            "approved_date",
            "approved_date_eng",
            "status",
        )
        extra_kwargs = {
            "prepared_by": {"required": False, "allow_null": True}, 
            "is_prepared": {"required": False, "allow_null": True}, 
            "prepared_date": {"required": False, "allow_null": True}, 
            "prepared_date_eng": {"required": False, "allow_null": True}, 
            "verified_by": {"required": False, "allow_null": True}, 
            "is_verified": {"required": False, "allow_null": True}, 
            "verified_date": {"required": False, "allow_null": True}, 
            "verified_date_eng": {"required": False, "allow_null": True}, 
            "approved_by": {"required": False, "allow_null": True}, 
            "is_approved": {"required": False, "allow_null": True}, 
            "approved_date": {"required": False, "allow_null": True}, 
            "approved_date_eng": {"required": False, "allow_null": True}, 
            "status": {"required": False, "allow_null": True}, 
        }


class ApproveProcessSerializerView(serializers.ModelSerializer):
    prepared_by = EmployeeSerializer(read_only=True)
    verified_by = EmployeeSerializer(read_only=True)
    approved_by = EmployeeSerializer(read_only=True)

    class Meta:
        model = ApproveProcess
        fields = (
            "prepared_by",
            "is_prepared",
            "prepared_date",
            "prepared_date_eng",
            "verified_by",
            "is_verified",
            "verified_date",
            "verified_date_eng",
            "approved_by",
            "is_approved",
            "approved_date",
            "approved_date_eng",
            "status",
        )
        extra_kwargs = {
            "prepared_by": {"required": False, "allow_null": True}, 
            "is_prepared": {"required": False, "allow_null": True}, 
            "prepared_date": {"required": False, "allow_null": True}, 
            "prepared_date_eng": {"required": False, "allow_null": True}, 
            "verified_by": {"required": False, "allow_null": True}, 
            "is_verified": {"required": False, "allow_null": True}, 
            "verified_date": {"required": False, "allow_null": True}, 
            "verified_date_eng": {"required": False, "allow_null": True}, 
            "approved_by": {"required": False, "allow_null": True}, 
            "is_approved": {"required": False, "allow_null": True}, 
            "approved_date": {"required": False, "allow_null": True}, 
            "approved_date_eng": {"required": False, "allow_null": True}, 
            "status": {"required": False, "allow_null": True}, 
        }

class IncomeExpenseDetermineSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeExpenseDetermine
        fields = (
            "financial_year",
            "estimated_amount",
            "date",
            "date_eng",
            "status",
        )
        extra_kwargs = {
            "financial_year": {"required": False, "allow_null": True},
            "estimated_amount": {"required": False, "allow_null": True},
            "date": {"required": False, "allow_null": True},
            "date_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

class ExpenseRangeDetermineSerializer(IncomeExpenseDetermineSerializer):
    class Meta:
        model = ExpenseBudgetRangeDetermine
        fields = IncomeExpenseDetermineSerializer.Meta.fields + (
            "id",
            "expense_determine_level",
            "ward",
            "expense_title_no",
            "parent",
            "source_type",
            "approve_process",
            "status",
            "is_budget_estimates",
        )
        extra_kwargs = {
            "expense_determine_level": {"required": False, "allow_null": True}, 
            "ward": {"required": False, "allow_null": True}, 
            "expense_title_no": {"required": False, "allow_null": True}, 
            "parent": {"required": False, "allow_null": True}, 
            "source_type": {"required": False, "allow_null": True}, 
            "approve_process": {"required": False, "allow_null": True}, 
            "status": {"required": False, "allow_null": True}, 
            "is_budget_estimates": {"required": False, "allow_null": True}, 
        }

class IncomeRangeDetermineSerializer(IncomeExpenseDetermineSerializer):
    class Meta:
        model = IncomeExpenseDetermine
        fields = IncomeExpenseDetermineSerializer.Meta.fields + (
            "id",
            "income_title_no",
            "parent",
            "source_type",
            "approve_process",
            "status",
        )
        extra_kwargs = {
            "income_title_no": {"required": False, "allow_null": True},
            "parent": {"required": False, "allow_null": True},
            "source_type": {"required": False, "allow_null": True},
            "approve_process": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

class EFASerializer(IncomeExpenseDetermineSerializer):
    class Meta:
        model = IncomeExpenseDetermine
        fields = IncomeExpenseDetermineSerializer.Meta.fields + (
            "id",
            "income_title_no",
            "parent",
            "approve_process",
            "status",
        )
        extra_kwargs = {
            "income_title_no": {"required": False, "allow_null": True},
            "parent": {"required": False, "allow_null": True},
            "approve_process": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

class ExpenseRangeDetermineCreateSerializer(ExpenseRangeDetermineSerializer):
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ExpenseBudgetRangeDetermine.objects.all(), required=False
    )
    source_type = SourceSerializer()
    approve_process = ApproveProcessSerializer()

    class Meta:
        model = ExpenseBudgetRangeDetermine
        fields = ExpenseRangeDetermineSerializer.Meta.fields

    def create(self, validated_data):
        source_type_data = validated_data.pop("source_type")
        approve_process_data = validated_data.pop("approve_process")

        source_type = Source.objects.create(**source_type_data)
        approve_process = ApproveProcess.objects.create(**approve_process_data)

        validated_data["source_type"] = source_type
        validated_data["approve_process"] = approve_process

        office_detail = ExpenseBudgetRangeDetermine.objects.create(**validated_data)
        return office_detail


class ExpenseRangeDetermineViewSerializer(ExpenseRangeDetermineSerializer):
    financial_year = FinancialYearSerializer(read_only=True)
    parent = ExpenseRangeDetermineCreateSerializer(read_only=True)
    source_type = SourceSerializer(read_only=True)
    approve_process = ApproveProcessSerializer(read_only=True)

    class Meta:
        model = ExpenseBudgetRangeDetermine
        fields = ExpenseRangeDetermineSerializer.Meta.fields

    def get_financial_year(self, obj):
        if obj.financial_year:
            return FinancialYearSerializer(obj.financial_year).data
        return None

    def get_parent(self, obj):
        if obj.parent:
            return ExpenseRangeDetermineCreateSerializer(obj.parent)
        return None

    def get_source_type(self, obj):
        if obj.source_type:
            return SourceSerializer(obj.source_type).data
        return None

    def get_approve_process(self, obj):
        if obj.approve_process:
            return ApproveProcessSerializer(obj.approve_process).data
        return None


class IncomeRangeDetermineCreateSerializer(IncomeRangeDetermineSerializer):
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=IncomeBudgetRangeDetermine.objects.all(), required=False
    )
    source_type = SourceSerializer()
    approve_process = ApproveProcessSerializer()

    class Meta:
        model = IncomeBudgetRangeDetermine
        fields = IncomeRangeDetermineSerializer.Meta.fields

    def create(self, validated_data):
        source_type_data = validated_data.pop("source_type")
        approve_process_data = validated_data.pop("approve_process")

        source_type = Source.objects.create(**source_type_data)
        approve_process = ApproveProcess.objects.create(**approve_process_data)

        validated_data["source_type"] = source_type
        validated_data["approve_process"] = approve_process

        office_detail = IncomeBudgetRangeDetermine.objects.create(**validated_data)
        return office_detail


class IncomeRangeDetermineViewSerializer(IncomeRangeDetermineSerializer):
    financial_year = FinancialYearSerializer(read_only=True)
    parent = IncomeRangeDetermineCreateSerializer(read_only=True)
    source_type = SourceSerializer(read_only=True)
    approve_process = ApproveProcessSerializer(read_only=True)

    class Meta:
        model = IncomeBudgetRangeDetermine
        fields = IncomeRangeDetermineSerializer.Meta.fields

    def get_financial_year(self, obj):
        if obj.financial_year:
            return FinancialYearSerializer(obj.financial_year).data
        return None

    def get_parent(self, obj):
        if obj.parent:
            return IncomeRangeDetermineSerializer(obj.parent)
        return None

    def get_source_type(self, obj):
        if obj.source_type:
            return SourceSerializer(obj.source_type).data
        return None

    def get_approve_process(self, obj):
        if obj.approve_process:
            return ApproveProcessSerializer(obj.approve_process).data
        return None


class EFACreateSerializer(EFASerializer):
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=EstimateFinancialArrangements.objects.all(), required=False
    )
    approve_process = ApproveProcessSerializer()

    class Meta:
        model = EstimateFinancialArrangements
        fields = EFASerializer.Meta.fields

    def create(self, validated_data):
        approve_process_data = validated_data.pop("approve_process")
        approve_process = ApproveProcess.objects.create(**approve_process_data)
        validated_data["approve_process"] = approve_process
        office_detail = EstimateFinancialArrangements.objects.create(**validated_data)
        return office_detail

    def update(self, instance, validated_data):
        approval_process_data = validated_data.pop("approve_process")
        print(approval_process_data.get("approved_by", None), 8989898900000000)
        pb = approval_process_data.get("prepared_by", None)
        vb = approval_process_data.get("verified_by", None)
        ab = approval_process_data.get("approved_by", None)
        if pb:
            approval_process_data["prepared_by"] = pb.id
        if vb:
            approval_process_data["verified_by"] = vb.id
        if ab:
            approval_process_data["approved_by"] = ab.id
        if approval_process_data:
            approve_process_serializer = ApproveProcessSerializer(
                instance.approve_process, data=approval_process_data
            )
            if approve_process_serializer.is_valid():
                approve_process = approve_process_serializer.save()
                validated_data["approve_process"] = approve_process
            else:
                print(approve_process_serializer.errors)
        return super().update(instance, validated_data)


class EFAViewSerializer(EFASerializer):
    financial_year = FinancialYearSerializer(read_only=True)
    parent = EFACreateSerializer(read_only=True)
    approve_process = ApproveProcessSerializerView(read_only=True)

    class Meta:
        model = EstimateFinancialArrangements
        fields = EFASerializer.Meta.fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def get_employee_data(self, data):
        return {"id": data.id, "name": f"{data.first_name} {data.last_name}"}


class BudgetExpenseManagementSerializer(serializers.ModelSerializer):
    expense_title = serializers.PrimaryKeyRelatedField(
        queryset=AccountTitleManagement.objects.all(), required=False
    )
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False
    )
    sub_module = serializers.PrimaryKeyRelatedField(
        queryset=SubModule.objects.all(), required=False
    )
    revised_sub_module = serializers.PrimaryKeyRelatedField(
        queryset=SubModule.objects.all(), required=False
    )
    revised_financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False
    )
    budget_source = serializers.PrimaryKeyRelatedField(
        queryset=BudgetSource.objects.all(), required=False
    )
    subject_area = serializers.PrimaryKeyRelatedField(
        queryset=SubjectArea.objects.all(), required=False
    )
    approval_process = ApproveProcessSerializer()

    class Meta:
        model = BudgetExpenseManagement
        fields = (
            "id",
            "expense_title",
            "sub_module",
            "budget_source",
            "financial_year",
            "first_quarter",
            "second_quarter",
            "third_quarter",
            "forth_quarter",
            "estimated_expense_amount",
            "revised_sub_module",
            "revised_expense_amount",
            "revision_reason",
            "revised_financial_year",
            "subject_area",
            "status",
            "activity_name",
            "aim",
            "unit",
            "approval_process",
        )
        extra_kwargs = {
            "expense_title": {"required": False, "allow_null": True},
            "sub_module": {"required": False, "allow_null": True},
            "budget_source": {"required": False, "allow_null": True},
            "financial_year": {"required": False, "allow_null": True},
            "first_quarter": {"required": False, "allow_null": True},
            "second_quarter": {"required": False, "allow_null": True},
            "third_quarter": {"required": False, "allow_null": True},
            "forth_quarter": {"required": False, "allow_null": True},
            "estimated_expense_amount": {"required": False, "allow_null": True},
            "revised_sub_module": {"required": False, "allow_null": True},
            "revised_expense_amount": {"required": False, "allow_null": True},
            "revision_reason": {"required": False, "allow_null": True},
            "revised_financial_year": {"required": False, "allow_null": True},
            "subject_area": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "activity_name": {"required": False, "allow_null": True},
            "aim": {"required": False, "allow_null": True},
            "unit": {"required": False, "allow_null": True},
            "approval_process": {"required": False, "allow_null": True},
        }
    def create(self, validated_data):
        approval_process_data = validated_data.pop("approval_process")
        approval_process = ApproveProcess.objects.create(**approval_process_data)
        validated_data["approval_process"] = approval_process
        bem = BudgetExpenseManagement.objects.create(**validated_data)
        return bem

    def update(self, instance, validated_data):
        try:
            approval_process_data = validated_data.pop("approval_process")
            approval_process_data["prepared_by"] = approval_process_data.pop(
                "prepared_by"
            ).id
            approval_process_data["verified_by"] = approval_process_data.pop(
                "verified_by"
            ).id
            approval_process_data["approved_by"] = approval_process_data.pop(
                "approved_by"
            ).id
            if approval_process_data:
                approve_process_serializer = ApproveProcessSerializer(
                    instance.approval_process, data=approval_process_data
                )
                if approve_process_serializer.is_valid():
                    approve_process = approve_process_serializer.save()
                    validated_data["approval_process"] = approve_process
                else:
                    print(approve_process_serializer.errors)
            return super().update(instance, validated_data)
        except Exception as e:
            raise serializers.ValidationError(e)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        expense_title = instance.expense_title
        financial_year = instance.financial_year
        sub_module = instance.sub_module
        budget_source = instance.budget_source
        approval_process = instance.approval_process
        subject_area = instance.subject_area
        revised_sub_module = instance.revised_sub_module
        revised_financial_year = instance.revised_financial_year
        if expense_title:
            representation["expense_title"] = {
                "id": expense_title.id,
                "expense_title_number": expense_title.code,
            }
        else:
            representation["expense_title"] = None
        if financial_year:
            representation["financial_year"] = {
                "id": financial_year.id,
                "name": financial_year.start_year,
                "name_eng": financial_year.end_year,
                "fy": financial_year.fy,
            }
        else:
            representation["financial_year"] = None

        if revised_financial_year:
            representation["revised_financial_year"] = {
                "id": revised_financial_year.id,
                "name": revised_financial_year.start_year,
                "name_eng": revised_financial_year.end_year,
                "fy": revised_financial_year.fy,
            }
        else:
            representation["revised_financial_year"] = None
        if sub_module:
            representation["sub_module"] = {
                "id": sub_module.id,
                "name": sub_module.name,
                "name_eng": sub_module.name_eng,
            }
        else:
            representation["sub_module"] = None
        if revised_sub_module:
            representation["revised_sub_module"] = {
                "id": revised_sub_module.id,
                "name": revised_sub_module.name,
                "name_eng": revised_sub_module.name_eng,
            }
        else:
            representation["revised_sub_module"] = None
        if budget_source:
            representation["budget_source"] = {
                "id": budget_source.id,
                "phone_number": budget_source.phone_number,
                "email": budget_source.email,
                "country": budget_source.country,
                "address": budget_source.address,
            }
        else:
            representation["budget_source"] = None
        if subject_area:
            representation["subject_area"] = {
                "id": subject_area.id,
                "code": subject_area.code,
                "name": subject_area.name,
                "name_eng": subject_area.name_eng,
                "status": subject_area.status,
            }
        else:
            representation["subject_area"] = None
        if approval_process:
            if approval_process.prepared_by:
                prepared_by = {
                    "id": approval_process.prepared_by.id,
                    "name": approval_process.prepared_by.first_name
                    + " "
                    + approval_process.prepared_by.last_name,
                }
            else:
                prepared_by = {}
            if approval_process.verified_by:
                verified_by = {
                    "id": approval_process.verified_by.id,
                    "name": approval_process.verified_by.first_name
                    + " "
                    + approval_process.verified_by.last_name,
                }
            else:
                verified_by = {}
            if approval_process.approved_by:
                approved_by = {
                    "id": approval_process.approved_by.id,
                    "name": approval_process.approved_by.first_name
                    + " "
                    + approval_process.approved_by.last_name,
                }
            else:
                approved_by = {}
            is_prepared = approval_process.is_prepared
            is_verified = approval_process.is_verified
            is_approved = approval_process.is_approved
            representation["approval_process"] = {
                "id": approval_process.id,
                "prepared_by": prepared_by,
                "prepared_date": approval_process.prepared_date,
                "prepared_date_eng": approval_process.prepared_date_eng,
                "verified_by": verified_by,
                "is_prepared": is_prepared,
                "is_verified": is_verified,
                "is_approved": is_approved,
                "verified_date": approval_process.verified_date,
                "verified_date_eng": approval_process.verified_date_eng,
                "approved_by": approved_by,
                "approved_date": approval_process.approved_date,
                "approved_date_eng": approval_process.approved_date_eng,
            }
        else:
            representation["approval_process"] = None
        return representation


class BudgetTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetTransfer
        fields = "__all__"
        read_only_fields = ["id", "display_order", "allocation_id"]

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.display_order = instance.id
        instance.allocation_id = instance.id
        instance.save()
        return instance


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        if value == "" and self.allow_blank:
            return value

        if value == "":
            return None

    def to_internal_value(self, data):
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class BudgetManagementSeralizer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "value",
            "acc_id",
        )
        extra_kwargs = {
            "value": {"required": False, "allow_null": True},
            "acc_id": {"required": False, "allow_null": True},
        }
        model = BudgetManagement

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["text"] = f"{representation['id']} - {representation['value']}"
        return representation


class BudgetAmmendmentSerializer(serializers.ModelSerializer):
    sub_module = serializers.PrimaryKeyRelatedField(
        queryset=SubModule.objects.all(), required=False
    )
    budget_source = serializers.PrimaryKeyRelatedField(
        queryset=BudgetSource.objects.all(), required=False
    )
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False
    )
    account_title = serializers.PrimaryKeyRelatedField(
        queryset=AccountTitleManagement.objects.all(), required=False
    )
    budget_management = serializers.PrimaryKeyRelatedField(
        queryset=BudgetManagement.objects.all(), required=False
    )

    class Meta:
        fields = (
            "sub_module",
            "budget_source",
            "financial_year",
            "account_title",
            "allocation_type",
            "kramagat",
            "status",
            "from_year",
            "from_year_eng",
            "description",
            "budget_management",
            "rakam",
        )
        extra_kwargs = {
            "sub_module": {"required": False, "allow_null": True},
            "budget_source": {"required": False, "allow_null": True},
            "financial_year": {"required": False, "allow_null": True},
            "account_title": {"required": False, "allow_null": True},
            "allocation_type": {"required": False, "allow_null": True},
            "kramagat": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "from_year": {"required": False, "allow_null": True},
            "from_year_eng": {"required": False, "allow_null": True},
            "description": {"required": False, "allow_null": True},
            "budget_management": {"required": False, "allow_null": True},
            "rakam": {"required": False, "allow_null": True},
        }
        model = BudgetAmmendment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        budget_source = instance.budget_source
        financial_year = instance.financial_year
        sub_module = instance.sub_module
        account_title = instance.account_title
        budget_management = instance.budget_management

        if budget_source:
            representation["budget_source"] = {
                "id": budget_source.id,
                "phone_number": budget_source.phone_number,
                "email": budget_source.email,
                "country": budget_source.country,
                "address": budget_source.address,
            }
        else:
            representation["budget_source"] = None

        if financial_year:
            representation["financial_year"] = {
                "id": financial_year.id,
                "name": financial_year.start_year,
                "name_eng": financial_year.end_year,
                "fy": financial_year.fy,
            }
        else:
            representation["financial_year"] = None
        if sub_module:
            representation["sub_module"] = {
                "id": sub_module.id,
                "name": sub_module.name,
                "name_eng": sub_module.name_eng,
            }
        else:
            representation["sub_module"] = None

        if account_title:
            representation["account_title"] = {
                "id": account_title.id,
                "name": account_title.display_name,
                "name_eng": account_title.display_name_eng,
            }
        else:
            representation["account_title"] = None

        if budget_management:
            representation["budget_management"] = {
                "id": budget_management.id,
                "value": budget_management.value,
                "acc_id": budget_management.acc_id,
            }
        else:
            representation["budget_management"] = None

        return representation
