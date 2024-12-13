import json

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import exceptions, serializers

from base_model.base_serializers import (
    BaseSerializer,
    WriteableNestedModelBaseSerializer,
)
from base_model.models import Address
from base_model.serializers import AddressSerializer
from employee.models import Department, Employee, EmployeeSector, Position
from employee.serializers import CommonSerializer, EmployeeSectorSerializer
from formulate_plan.models import WorkClass
from plan_execution.choices import (
    CommentSentForChoices,
    CommentStatusChoices,
    ProcessNameChoices,
)
from plan_execution.models import (
    AccountingTopic,
    BailType,
    BenefitedDetail,
    BudgetAllocationDetail,
    BuildingMaterialDetail,
    CommentAndOrder,
    ConsumerFormulation,
    CostEstimateData,
    DepositMandate,
    EstimationSubmitAcceptance,
    ExpenseTypeDetail,
    FirmQuotedCostEstimate,
    IndividualProjectComment,
    InstallmentDetail,
    InstitutionalCollaborationMandate,
    InstitutionalCollaborationNominatedStaff,
    MaintenanceArrangement,
    MeasuringBook,
    MonitoringCommitteeDetail,
    OfficialProcess,
    OfficialProcessRemarkFile,
    OpeningContractAccount,
    PaymentDetail,
    PaymentExitBill,
    PlanStartDecision,
    ProbabilityStudyApprove,
    ProjectAgreement,
    ProjectBidCollection,
    ProjectComment,
    ProjectCommentRemarkFile,
    ProjectDarbhauBid,
    ProjectDeadline,
    ProjectExecution,
    ProjectExecutionDocument,
    ProjectFinishedBailReturn,
    ProjectInstallment,
    ProjectMobilization,
    ProjectMobilizationDetail,
    ProjectPhysicalDescription,
    ProjectReportFinishedAndUpdate,
    ProjectRevision,
    ProjectTask,
    ProjectTender,
    ProjectUnitDetail,
    QuotationFirmDetails,
    QuotationInvitationForProposal,
    QuotationSpecification,
    QuotationSubmissionApproval,
    StartPmsProcess,
    TenderPurchaseBranch,
    UserCommitteeDocuments,
    UserCommitteeMonitoring,
    UserCommitteeProjectWorkComplete,
)
from pms_system import settings
from pms_system.settings import MEDIA_URL
from project.models import FinancialYear, Municipality, Unit
from project.serializers import ProjectSerializer, SimpleMunicipalitySerializer
from project_planning.models import (
    BFI,
    AccountTitleManagement,
    BudgetSource,
    BudgetSubTitle,
    CollectPayment,
    ConstructionMaterialDescription,
    ConsumerCommittee,
    ConsumerCommitteeMember,
    ExpanseType,
    MemberType,
    MonitoringCommittee,
    NewsPaper,
    Organization,
    PaymentMedium,
    PriorityType,
    Program,
    ProjectActivity,
    ProjectLevel,
    ProjectNature,
    ProjectStartDecision,
    ProjectType,
    PurposePlan,
    SelectionFeasibility,
    SourceReceipt,
    StrategicSign,
    SubjectArea,
)
from project_planning.serializers import MonitoringCommitteeMemberSerializer
from user.models import User
from utils.constants import ProcessStatus, RequestSend
from utils.nepali_date import ad_to_bs


class PlanExecutionBaseSerializer(WritableNestedModelSerializer):

    def save(self, **kwargs):
        updated_kwargs = kwargs.copy()
        if self.context.get("request"):
            if not self.instance:
                updated_kwargs["created_by"] = self.context["request"].user
            else:
                updated_kwargs["updated_by"] = self.context["request"].user
        return super().save(**updated_kwargs)

    def get_fields(self):
        fields = dict(super().get_fields())
        for field_name, field_class in fields.items():
            field_class.required = False
            field_class.allow_null = True
            field_class.allow_blank = True
        return fields

    def get_bank_data(self, data):
        if not data:
            return None
        return {
            "id": data.id,
            "code": data.code,
            "full_name": data.full_name,
            "full_name_eng": data.full_name_eng,
            "registration_no": data.registration_no,
            "registration_date": data.registration_date,
            "registration_date_eng": data.registration_date_eng,
            "bank_type": data.bank_type.name if data.bank_type else "",
            "cheque_format": data.cheque_format.name if data.cheque_format else "",
        }

    def employee_data(self, data):
        if not data:
            return None
        return {
            "id": data.id,
            "code": data.code,
            "full_name": data.full_name,
            "full_name_eng": data.full_name_eng,
        }

    def get_address_data(self, data):
        if not data:
            return None
        return {
            "municipality": (
                self.get_municipality(data.municipality) if data.municipality else None
            ),
            "ward": data.ward,
            "ward_eng": data.ward_eng,
        }

    def get_municipality(self, municipality):
        if not municipality:
            return None
        return {
            "id": municipality.id,
            "name": municipality.name,
            "name_eng": municipality.name_eng,
        }

    def get_common_data(self, data):
        if not data:
            return None
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": str(data.name_eng),
            "code": str(data.code),
        }


class StartPmsProcessSerializer(CommonSerializer):
    class Meta:
        model = StartPmsProcess
        fields = CommonSerializer.Meta.fields


class PlanStartDecisionSerializer(CommonSerializer):
    class Meta:
        model = PlanStartDecision
        fields = CommonSerializer.Meta.fields


class ProjectExecutionSerializer(PlanExecutionBaseSerializer):
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False, allow_null=True
    )
    address = AddressSerializer(required=False, allow_null=True)
    project_type = serializers.PrimaryKeyRelatedField(
        queryset=ProjectType.objects.all(), required=False, allow_null=True
    )
    project_nature = serializers.PrimaryKeyRelatedField(
        queryset=ProjectNature.objects.all(), required=False, allow_null=True
    )
    work_class = serializers.PrimaryKeyRelatedField(
        queryset=WorkClass.objects.all(), required=False, allow_null=True
    )
    subject_area = serializers.PrimaryKeyRelatedField(
        queryset=SubjectArea.objects.all(), required=False, allow_null=True
    )
    strategic_sign = serializers.PrimaryKeyRelatedField(
        queryset=StrategicSign.objects.all(), required=False, allow_null=True
    )
    project = ProjectSerializer(read_only=True)
    program = serializers.PrimaryKeyRelatedField(
        queryset=Program.objects.all(), required=False, allow_null=True
    )
    project_priority = serializers.PrimaryKeyRelatedField(
        queryset=PriorityType.objects.all(), required=False, allow_null=True
    )
    start_pms_process = serializers.PrimaryKeyRelatedField(
        queryset=StartPmsProcess.objects.all(), required=False, allow_null=True
    )
    plan_start_decision = serializers.PrimaryKeyRelatedField(
        queryset=PlanStartDecision.objects.all(), required=False, allow_null=True
    )
    project_level = serializers.PrimaryKeyRelatedField(
        queryset=ProjectLevel.objects.all(), required=False, allow_null=True
    )
    work_area = serializers.PrimaryKeyRelatedField(
        queryset=SubjectArea.objects.all(), required=False, allow_null=True
    )
    purpose = serializers.PrimaryKeyRelatedField(
        queryset=PurposePlan.objects.all(), required=False, allow_null=True
    )

    def validate(self, attrs):
        # if (
        #     attrs.get("name", "empty") is None
        #     and attrs.get("name_eng", "empty") is None
        # ):
        #     raise exceptions.ValidationError(
        #         {
        #             "name": "Either enter name or english name",
        #             "name_eng": "Either enter name or english name",
        #         }
        #     )

        # if attrs.get("code", None) is None:
        #     raise exceptions.ValidationError({"code": "This cannot be null"})

        return super().validate(attrs)

    class Meta:
        model = ProjectExecution
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "financial_year",
            "phase",
            "ward",
            "address",
            "project_type",
            "project_nature",
            "work_class",
            "subject_area",
            "work_area",
            "purpose",
            "strategic_sign",
            "work_proposer_type",  # Constant
            "program",
            "project_priority",
            "start_pms_process",
            "plan_start_decision",
            "project_level",
            "first_trimester",
            "second_trimester",
            "third_trimester",
            "fourth_trimester",
            "is_multi_year_plan",
            "first_year",
            "second_year",
            "third_year",
            "forth_year",
            "fifth_year",
            "benefited_households",
            "benefited_population",
            "other",
            "latitude",
            "longitude",
            "appropriated_amount",
            "overhead",
            "total_committee_members",
            "total_gathered_organizations",
            "contingency",
            "contingency_percent",
            "mu_aa_ka",
            "project",
            "mu_aa_ka_percent",
            "public_charity",
            "public_charity_percent",
            "maintenance",
            "maintenance_percent",
            "disaster_mgmt_fund",
            "disaster_mgmt_fund_percent",
            "total_estimate",
            "subtotal_estimate",
            "self_payment",
            "status",
            "remarks",
            "kramagat",
        )
        read_only_fields = ("id", "project")
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "financial_year": {"required": False, "allow_null": True},
            "ward": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
            "project_type": {"required": False, "allow_null": True},
            "project_nature": {"required": False, "allow_null": True},
            "work_class": {"required": False, "allow_null": True},
            "subject_area": {"required": False, "allow_null": True},
            "strategic_sign": {"required": False, "allow_null": True},
            "work_proposer_type": {"required": False, "allow_null": True},
            "program": {"required": False, "allow_null": True},
            "project_priority": {"required": False, "allow_null": True},
            "start_pms_process": {"required": False, "allow_null": True},
            "plan_start_decision": {"required": False, "allow_null": True},
            "project_level": {"required": False, "allow_null": True},
            "first_trimester": {"required": False, "allow_null": True},
            "second_trimester": {"required": False, "allow_null": True},
            "third_trimester": {"required": False, "allow_null": True},
            "fourth_trimester": {"required": False, "allow_null": True},
            "is_multi_year_plan": {"required": False, "allow_null": True},
            "first_year": {"required": False, "allow_null": True},
            "second_year": {"required": False, "allow_null": True},
            "third_year": {"required": False, "allow_null": True},
            "forth_year": {"required": False, "allow_null": True},
            "fifth_year": {"required": False, "allow_null": True},
            "benefited_households": {"required": False, "allow_null": True},
            "benefited_population": {"required": False, "allow_null": True},
            "other": {"required": False, "allow_null": True},
            "latitude": {"required": False, "allow_null": True},
            "longitude": {"required": False, "allow_null": True},
            "appropriated_amount": {"required": False, "allow_null": True},
            "overhead": {"required": False, "allow_null": True},
            "total_committee_members": {"required": False, "allow_null": True},
            "total_gathered_organizations": {"required": False, "allow_null": True},
            "contingency": {"required": False, "allow_null": True},
            "contingency_percent": {"required": False, "allow_null": True},
            "mu_aa_ka": {"required": False, "allow_null": True},
            "mu_aa_ka_percent": {"required": False, "allow_null": True},
            "public_charity": {"required": False, "allow_null": True},
            "public_charity_percent": {"required": False, "allow_null": True},
            "maintenance": {"required": False, "allow_null": True},
            "maintenance_percent": {"required": False, "allow_null": True},
            "total_estimate": {"required": False, "allow_null": True},
            "subtotal_estimate": {"required": False, "allow_null": True},
            "self_payment": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "kramagat": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        if address_data:
            address = Address.objects.create(**address_data)
            validated_data["address"] = address
        project_execution = ProjectExecution.objects.create(**validated_data)
        return project_execution

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)

        if address_data:
            address_data = AddressSerializer.correct_data(address_data)
            address_serializer = AddressSerializer(instance.address, data=address_data)

            if address_serializer.is_valid():
                address = address_serializer.save()
                validated_data["address"] = address

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        financial_year = instance.financial_year
        work_class = instance.work_class
        project_type = instance.project_type
        project_level = instance.project_level
        purpose = instance.purpose
        project_nature = instance.project_nature
        subject_area = instance.subject_area
        work_area = instance.work_area
        strategic_sign = instance.strategic_sign
        program = instance.program
        project_priority = instance.project_priority
        start_pms_process = instance.start_pms_process
        plan_start_decision = instance.plan_start_decision
        selected_consumer_committee = instance.selected_consumer_committee
        representation["financial_year"] = (
            self.get_fiscal_year(financial_year) if financial_year else None
        )
        # representation["address"] = (
        #     self.get_common_data(address) if address else None
        # )
        representation["project_type"] = (
            self.get_common_data(project_type) if project_type else None
        )
        representation["work_class"] = (
            self.get_common_data(work_class) if work_class else None
        )
        representation["project_level"] = (
            self.get_common_data(project_level) if project_level else None
        )
        representation["purpose"] = self.get_common_data(purpose) if purpose else None
        representation["project_nature"] = (
            self.get_common_data(project_nature) if project_nature else None
        )
        representation["subject_area"] = (
            self.get_common_data(subject_area) if subject_area else None
        )
        representation["work_area"] = (
            self.get_common_data(work_area) if work_area else None
        )
        representation["strategic_sign"] = (
            self.get_common_data(strategic_sign) if strategic_sign else None
        )

        representation["program"] = self.get_common_data(program) if program else None
        representation["project_priority"] = (
            self.get_common_data(project_priority) if project_priority else None
        )
        representation["start_pms_process"] = (
            self.get_common_data(start_pms_process) if start_pms_process else None
        )
        representation["plan_start_decision"] = (
            self.get_common_data(plan_start_decision) if plan_start_decision else None
        )
        representation["selected_consumer_committee"] = (
            self.consumer_committee_data(selected_consumer_committee)
            if selected_consumer_committee
            else None
        )

        return representation

    def get_address_data(self, data):
        return {
            "municipality": (
                self.get_municipality(data.municipality) if data.municipality else None
            ),
            "ward": data.ward,
            "ward_eng": data.ward_eng,
        }

    def get_municipality(self, municipality):
        return {
            "id": municipality.id,
            "name": municipality.name,
            "name_eng": municipality.name_eng,
        }

    def get_fiscal_year(self, data):
        return {
            "id": data.id,
            "start_year": data.start_year,
            "end_year": data.end_year,
            "fy": data.fy,
        }

    def consumer_committee_data(self, data):
        return {
            "id": data.id,
            "code": data.code,
            "full_name": data.full_name,
            "full_name_eng": data.full_name_eng,
            "registration_no": data.registration_no,
        }


class ProjectExecutionListSerializer(PlanExecutionBaseSerializer):
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all(), required=False, allow_null=True
    )
    address = AddressSerializer(required=False, allow_null=True)
    project_type = serializers.PrimaryKeyRelatedField(
        queryset=ProjectType.objects.all(), required=False, allow_null=True
    )
    project_nature = serializers.PrimaryKeyRelatedField(
        queryset=ProjectNature.objects.all(), required=False, allow_null=True
    )
    work_class = serializers.PrimaryKeyRelatedField(
        queryset=WorkClass.objects.all(), required=False, allow_null=True
    )
    subject_area = serializers.PrimaryKeyRelatedField(
        queryset=SubjectArea.objects.all(), required=False, allow_null=True
    )
    strategic_sign = serializers.PrimaryKeyRelatedField(
        queryset=StrategicSign.objects.all(), required=False, allow_null=True
    )
    program = serializers.PrimaryKeyRelatedField(
        queryset=Program.objects.all(), required=False, allow_null=True
    )
    project_priority = serializers.PrimaryKeyRelatedField(
        queryset=PriorityType.objects.all(), required=False, allow_null=True
    )
    start_pms_process = serializers.PrimaryKeyRelatedField(
        queryset=StartPmsProcess.objects.all(), required=False, allow_null=True
    )
    plan_start_decision = serializers.PrimaryKeyRelatedField(
        queryset=PlanStartDecision.objects.all(), required=False, allow_null=True
    )
    project_level = serializers.PrimaryKeyRelatedField(
        queryset=ProjectLevel.objects.all(), required=False, allow_null=True
    )

    project = ProjectSerializer(required=False, allow_null=True)

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
        model = ProjectExecution
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "financial_year",
            "ward",
            "address",
            "project",
            "project_type",
            "project_nature",
            "work_class",
            "subject_area",
            "strategic_sign",
            "work_proposer_type",  # Constant
            "program",
            "project_priority",
            "start_pms_process",
            "plan_start_decision",
            "project_level",
            # "budget_assurance",
            "first_trimester",
            "second_trimester",
            "third_trimester",
            "fourth_trimester",
            "is_multi_year_plan",
            "first_year",
            "second_year",
            "third_year",
            "forth_year",
            "fifth_year",
            "benefited_households",
            "benefited_population",
            "other",
            "latitude",
            "longitude",
            "appropriated_amount",
            "overhead",
            "contingency",
            "mu_aa_ka",
            "public_charity",
            "maintenance",
            "disaster_mgmt_fund",
            "total_estimate",
            "self_payment",
            "status",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "financial_year": {"required": False, "allow_null": True},
            "ward": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "project_type": {"required": False, "allow_null": True},
            "project_nature": {"required": False, "allow_null": True},
            "work_class": {"required": False, "allow_null": True},
            "subject_area": {"required": False, "allow_null": True},
            "strategic_sign": {"required": False, "allow_null": True},
            "work_proposer_type": {"required": False, "allow_null": True},  # Constant
            "program": {"required": False, "allow_null": True},
            "project_priority": {"required": False, "allow_null": True},
            "start_pms_process": {"required": False, "allow_null": True},
            "plan_start_decision": {"required": False, "allow_null": True},
            "project_level": {"required": False, "allow_null": True},
            # "budget_assurance": {"required": False, "allow_null": True},
            "first_trimester": {"required": False, "allow_null": True},
            "second_trimester": {"required": False, "allow_null": True},
            "third_trimester": {"required": False, "allow_null": True},
            "fourth_trimester": {"required": False, "allow_null": True},
            "is_multi_year_plan": {"required": False, "allow_null": True},
            "first_year": {"required": False, "allow_null": True},
            "second_year": {"required": False, "allow_null": True},
            "third_year": {"required": False, "allow_null": True},
            "forth_year": {"required": False, "allow_null": True},
            "fifth_year": {"required": False, "allow_null": True},
            "benefited_households": {"required": False, "allow_null": True},
            "benefited_population": {"required": False, "allow_null": True},
            "other": {"required": False, "allow_null": True},
            "latitude": {"required": False, "allow_null": True},
            "longitude": {"required": False, "allow_null": True},
            "appropriated_amount": {"required": False, "allow_null": True},
            "overhead": {"required": False, "allow_null": True},
            "contingency": {"required": False, "allow_null": True},
            "mu_aa_ka": {"required": False, "allow_null": True},
            "public_charity": {"required": False, "allow_null": True},
            "maintenance": {"required": False, "allow_null": True},
            "disaster_mgmt_fund": {"required": False, "allow_null": True},
            "total_estimate": {"required": False, "allow_null": True},
            "self_payment": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        read_only_fields = ("id", "project")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        financial_year = instance.financial_year
        address = instance.address
        work_class = instance.work_class
        project_type = instance.project_type
        project_level = instance.project_level
        project_nature = instance.project_nature
        subject_area = instance.subject_area
        strategic_sign = instance.strategic_sign
        program = instance.program
        project_priority = instance.project_priority
        start_pms_process = instance.start_pms_process
        plan_start_decision = instance.plan_start_decision
        representation["financial_year"] = (
            self.get_fiscal_year(financial_year) if financial_year else None
        )
        # representation["address"] = (
        #     self.get_common_data(address) if address else None
        # )
        representation["project_type"] = (
            self.get_common_data(project_type) if project_type else None
        )
        representation["address"] = self.get_address_data(address) if address else None
        representation["work_class"] = (
            self.get_common_data(work_class) if work_class else None
        )
        representation["project_nature"] = (
            self.get_common_data(project_nature) if project_nature else None
        )
        representation["subject_area"] = (
            self.get_common_data(subject_area) if subject_area else None
        )
        representation["strategic_sign"] = (
            self.get_common_data(strategic_sign) if strategic_sign else None
        )

        representation["program"] = self.get_common_data(program) if program else None
        representation["project_priority"] = (
            self.get_common_data(project_priority) if project_priority else None
        )
        representation["start_pms_process"] = (
            self.get_common_data(start_pms_process) if start_pms_process else None
        )
        representation["plan_start_decision"] = (
            self.get_common_data(plan_start_decision) if plan_start_decision else None
        )
        representation["project_level"] = (
            self.get_common_data(project_level) if project_level else None
        )
        return representation

    def get_address_data(self, data):
        try:
            return {
                "municipality": (
                    self.get_municipality(data.municipality)
                    if data.municipality
                    else None
                ),
                "district": (
                    self.get_district(data.municipality) if data.municipality else None
                ),
                "province": (
                    self.get_province(data.municipality) if data.municipality else None
                ),
                "ward": data.ward,
                "house_no": data.house_no,
                "tole": data.tole,
                "tole_eng": data.tole_eng,
                "road_name": data.road_name,
                "road_name_eng": data.road_name_eng,
            }
        except Exception as e:
            return None

    def get_municipality(self, municipality):
        try:
            return {
                "id": municipality.id,
                "name": municipality.name,
                "name_eng": municipality.name_eng,
            }
        except Exception as e:
            return None

    def get_district(self, mun_district):
        try:
            if mun_district:
                return {
                    "id": mun_district.district.id,
                    "name": mun_district.district.name,
                    "name_eng": mun_district.district.name_eng,
                }
            else:
                return None
        except Exception as e:
            print(e, "District...")
            return None

    def get_province(self, mun_province):
        try:
            if mun_province:
                if mun_province.district:
                    return {
                        "id": mun_province.district.province.id,
                        "name": mun_province.district.province.name,
                        "name_eng": mun_province.district.province.name_eng,
                    }
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(e, "Province...")
            return None

    def get_fiscal_year(self, data):
        return {
            "id": data.id,
            "start_year": data.start_year,
            "end_year": data.end_year,
            "fy": data.fy,
        }


class ProjectPhysicalDescriptionSerializer(PlanExecutionBaseSerializer):
    unit_type = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(), required=False, allow_null=True
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )

    class Meta:
        model = ProjectPhysicalDescription
        fields = ("id", "remarks", "unit", "status", "unit_type", "project")
        extra_kwargs = {
            "remarks": {"required": False, "allow_null": True},
            "unit": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "unit_type": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        unit_type = instance.unit_type
        representation["unit_type"] = (
            self.get_common_data(unit_type) if unit_type else None
        )
        project = instance.project
        representation["project"] = self.get_project_data(project) if project else None
        return representation

    def get_project_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
        }


class ProjectUnitDetailSerializer(PlanExecutionBaseSerializer):
    unit_type = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(), required=False, allow_null=True
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )

    class Meta:
        model = ProjectUnitDetail
        fields = (
            "id",
            "unit",
            "unit_rate",
            "total_unit",
            "project",
            "remark",
            "status",
            "unit_type",
        )
        extra_kwargs = {
            "unit": {"required": False, "allow_null": True},
            "unit_rate": {"required": False, "allow_null": True},
            "total_unit": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "remark": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "unit_type": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        unit_type = instance.unit_type
        representation["unit_type"] = (
            self.get_common_data(unit_type) if unit_type else None
        )
        project = instance.project
        representation["project"] = self.get_project_data(project) if project else None
        return representation

    def get_project_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
        }


class BudgetAllocationDetailSerializer(PlanExecutionBaseSerializer):
    budget_sub_title = serializers.PrimaryKeyRelatedField(
        queryset=BudgetSubTitle.objects.all(), required=False, allow_null=True
    )
    expense_title = serializers.PrimaryKeyRelatedField(
        queryset=AccountTitleManagement.objects.filter(module__name_eng="Expenditure"),
        required=False,
        allow_null=True,
    )
    subject_area = serializers.PrimaryKeyRelatedField(
        queryset=SubjectArea.objects.all(), required=False, allow_null=True
    )
    program = serializers.PrimaryKeyRelatedField(
        queryset=Program.objects.all(), required=False, allow_null=True
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    # budget_subject = serializers.PrimaryKeyRelatedField(
    #     queryset=BudgetSource.objects.all(), required=False, allow_null=True
    # )
    source_receipt = serializers.PrimaryKeyRelatedField(
        queryset=SourceReceipt.objects.all(), required=False, allow_null=True
    )
    expense_method = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMedium.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = BudgetAllocationDetail
        fields = (
            "id",
            "project",
            "budget_sub_title",
            "expense_title",
            "subject_area",
            "program",
            "budget_source",
            "source_receipt",
            "expense_method",
            "first_quarter",
            "second_quarter",
            "third_quarter",
            "fourth_quarter",
            "total",
            "multi_year_budget",
            "is_revise_budget",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "budget_sub_title": {"required": False, "allow_null": True},
            "expense_title": {"required": False, "allow_null": True},
            "subject_area": {"required": False, "allow_null": True},
            "program": {"required": False, "allow_null": True},
            "budget_source": {"required": False, "allow_null": True},
            "source_receipt": {"required": False, "allow_null": True},
            "expense_method": {"required": False, "allow_null": True},
            "first_quarter": {"required": False, "allow_null": True},
            "second_quarter": {"required": False, "allow_null": True},
            "third_quarter": {"required": False, "allow_null": True},
            "fourth_quarter": {"required": False, "allow_null": True},
            "total": {"required": False, "allow_null": True},
            "multi_year_budget": {"required": False, "allow_null": True},
            "is_revise_budget": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        budget_sub_title = instance.budget_sub_title
        expense_title = instance.expense_title
        subject_area = instance.subject_area
        program = instance.program
        budget_source = instance.budget_source
        source_receipt = instance.source_receipt
        expense_method = instance.expense_method
        # budget_subject = instance.budget_subject

        representation["project"] = self.get_project_data(project) if project else None
        representation["budget_sub_title"] = (
            self.get_common_data(budget_sub_title) if budget_sub_title else None
        )
        representation["expense_title"] = (
            self.get_atm_data(expense_title) if expense_title else None
        )
        representation["subject_area"] = (
            self.get_common_data(subject_area) if subject_area else None
        )
        representation["program"] = self.get_common_data(program) if program else None
        representation["budget_source"] = (
            self.get_budget_source(budget_source) if budget_source else None
        )
        representation["source_receipt"] = (
            self.get_common_data(source_receipt) if source_receipt else None
        )
        representation["expense_method"] = (
            self.get_common_data(expense_method) if expense_method else None
        )
        # representation["budget_subject"] = (
        #     self.get_common_data(budget_subject) if budget_subject else None
        # )
        return representation

    def get_project_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
        }

    def get_budget_source(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
            "phone_number": data.phone_number,
            "email": data.email,
        }

    def get_atm_data(self, data):
        return {
            "id": data.id,
            "code": data.code,
            "display_name": data.name,
            "display_name_eng": data.name_eng,
            "financial_year": (
                f"{data.financial_year.start_year}/{data.financial_year.end_year}"
                if data.financial_year
                else None
            ),
            "is_budgeted": data.is_budgeted,
        }


class BudgetAllocationDetailCreateSerializer(PlanExecutionBaseSerializer):
    """
    You sent
    label="व्यय शिर्षक नम्बर:"
                label="बजेट स्रोत:"
                label="आर्थिक वर्ष:"
                label="पहिलो त्रैमासिक:"
                label="दोस्रो त्रैमासिक:"
                label="अनुमानित व्यय रकम:"
                label="विषयगत कार्यक्षेत्र:"
                <label className="">स्थिति:</label>
                label="क्रियाकलापको नाम:"
                label="लक्ष:"
                label="इकाई:"
                label="पुनारवाकोलित व्यय रकम:"
                label="कारण:"
    """

    class Meta:
        model = BudgetAllocationDetail
        fields = (
            "expense_title",
            "budget_sub_title",
            "budget_source",
            "financial_year",
            "first_quarter",
            "second_quarter",
            "third_quarter",
            "fourth_quarter",
            "total",
            "subject_area",
            "status",
        )
        extra_kwargs = {
            "expense_title": {"required": False, "allow_null": True},
            "budget_sub_title": {"required": False, "allow_null": True},
            "budget_source": {"required": False, "allow_null": True},
            "financial_year": {"required": False, "allow_null": True},
            "first_quarter": {"required": False, "allow_null": True},
            "second_quarter": {"required": False, "allow_null": True},
            "third_quarter": {"required": False, "allow_null": True},
            "fourth_quarter": {"required": False, "allow_null": True},
            "total": {"required": False, "allow_null": True},
            "subject_area": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        return super().create(validated_data)


class ATMBudgetAllocationSerializer(PlanExecutionBaseSerializer):
    class Meta:
        model = AccountTitleManagement


class BenefitedDetailSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )

    class Meta:
        model = BenefitedDetail
        fields = (
            "id",
            "project",
            "target_group",
            "total_house_number",
            "total_man",
            "total_women",
            "total_other",
            "total_population",
            "remark",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "target_group": {"required": False, "allow_null": True},
            "total_house_number": {"required": False, "allow_null": True},
            "total_man": {"required": False, "allow_null": True},
            "total_women": {"required": False, "allow_null": True},
            "total_other": {"required": False, "allow_null": True},
            "total_population": {"required": False, "allow_null": True},
            "remark": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        target_group = instance.target_group
        representation["project"] = self.get_project_data(project) if project else None
        representation["target_group"] = (
            self.get_common_data(target_group) if target_group else None
        )
        return representation

    def get_project_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
        }


class ProjectTaskSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )

    class Meta:
        model = ProjectTask
        fields = (
            "id",
            "project",
            "task",
            "task_status",
            "weight",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "task": {"required": False, "allow_null": True},
            "task_status": {"required": False, "allow_null": True},
            "weight": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def validate_weight_data(self, weight, project_id):
        if weight > 100:
            raise serializers.ValidationError("Task Weight cannot be higher than 100%.")
        existing_tasks = ProjectTask.objects.filter(project=project_id)
        total_weight = sum(
            task.weight for task in existing_tasks if task.weight is not None
        )
        if total_weight + weight > 100:
            raise serializers.ValidationError(
                "Total weight for the project cannot exceed 100%."
            )
        return True

    def validate_update_weight_data(self, weight, project_id):
        existing_tasks = ProjectTask.objects.filter(project=project_id).exclude(
            pk=self.instance.pk
        )
        total_weight = sum(
            task.weight for task in existing_tasks if task.weight is not None
        )
        if total_weight + weight > 100:
            raise serializers.ValidationError(
                "Total weight for the project cannot exceed 100%."
            )
        return True

    def create(self, validated_data):
        project_id = validated_data["project"]
        weight = validated_data["weight"]
        validate_data = self.validate_weight_data(weight, project_id)
        validated_data["project"] = project_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        print(instance, 97832827400)
        project_id = validated_data["project"]
        weight = validated_data["weight"]
        validate_data = self.validate_update_weight_data(weight, project_id)
        validated_data["project"] = project_id
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        representation["project"] = self.get_project_data(project) if project else None
        return representation

    def get_project_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
        }


class TenderPurchaseBranchSerializer(CommonSerializer):
    class Meta:
        model = TenderPurchaseBranch
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "status",
            "detail",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }


class BailTypeSerializer(CommonSerializer):
    class Meta:
        model = BailType
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "status",
            "detail",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }


class AccountingTopicSerializer(CommonSerializer):
    class Meta:
        model = AccountingTopic
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "status",
            "detail",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }


class InstallmentSerializer(CommonSerializer):
    class Meta:
        model = ProjectInstallment
        fields = (
            "id",
            "code",
            "start_pms_process",
            "name",
            "name_eng",
            "status",
            "detail",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
        }


class ExpenseTypeDetailSerializer(PlanExecutionBaseSerializer):
    expense_type = serializers.PrimaryKeyRelatedField(
        queryset=ExpanseType.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ExpenseTypeDetail
        fields = (
            "id",
            "expense_type",
            "amount",
            "status",
            "remark",
        )
        extra_kwargs = {
            "expense_type": {"required": False, "allow_null": True},
            "amount": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "remark": {"required": False, "allow_null": True},
        }


class EstimationSubmitAcceptanceSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    estimated_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    cited_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    recommended_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    accounting_opinion_submitted_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    estimated_by_post = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    cited_by_post = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    recommended_by_post = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    accounting_opinion_submitted_by_post = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    approved_by_post = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = EstimationSubmitAcceptance
        fields = (
            "id",
            "project",
            "is_estimate_submitted",
            "estimated_by",
            "estimated_by_post",
            "estimate_date",
            "estimate_date_eng",
            "is_cited",
            "cited_by",
            "cited_by_post",
            "cited_date",
            "cited_date_eng",
            "is_recommended",
            "recommended_by",
            "recommended_by_post",
            "recommended_date",
            "recommended_date_eng",
            "is_accounting_opinion_submitted",
            "accounting_opinion_submitted_by",
            "accounting_opinion_submitted_by_post",
            "accounting_opinion_submitted_date",
            "accounting_opinion_submitted_date_eng",
            "accounting_opinion",
            "is_approved",
            "approved_by",
            "approved_by_post",
            "approved_date",
            "approved_date_eng",
            "approve_opinion",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "is_estimate_submitted": {"required": False, "allow_null": True},
            "estimated_by": {"required": False, "allow_null": True},
            "estimated_by_post": {"required": False, "allow_null": True},
            "estimate_date": {"required": False, "allow_null": True},
            "estimate_date_eng": {"required": False, "allow_null": True},
            "is_cited": {"required": False, "allow_null": True},
            "cited_by": {"required": False, "allow_null": True},
            "cited_by_post": {"required": False, "allow_null": True},
            "cited_date": {"required": False, "allow_null": True},
            "cited_date_eng": {"required": False, "allow_null": True},
            "is_recommended": {"required": False, "allow_null": True},
            "recommended_by": {"required": False, "allow_null": True},
            "recommended_by_post": {"required": False, "allow_null": True},
            "recommended_date": {"required": False, "allow_null": True},
            "recommended_date_eng": {"required": False, "allow_null": True},
            "is_accounting_opinion_submitted": {"required": False, "allow_null": True},
            "accounting_opinion_submitted_by": {"required": False, "allow_null": True},
            "accounting_opinion_submitted_by_post": {
                "required": False,
                "allow_null": True,
            },
            "accounting_opinion_submitted_date": {
                "required": False,
                "allow_null": True,
            },
            "accounting_opinion_submitted_date_eng": {
                "required": False,
                "allow_null": True,
            },
            "accounting_opinion": {"required": False, "allow_null": True},
            "is_approved": {"required": False, "allow_null": True},
            "approved_by": {"required": False, "allow_null": True},
            "approved_by_post": {"required": False, "allow_null": True},
            "approved_date": {"required": False, "allow_null": True},
            "approved_date_eng": {"required": False, "allow_null": True},
            "approve_opinion": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        estimated_by_data = instance.estimated_by
        cited_by_data = instance.cited_by
        recommended_by_data = instance.recommended_by
        accounting_opinion_submitted_by_data = instance.accounting_opinion_submitted_by
        approved_by_data = instance.approved_by
        estimated_by_post_data = instance.estimated_by_post
        cited_by_post_data = instance.cited_by_post
        recommended_by_post_data = instance.recommended_by_post
        accounting_opinion_submitted_by_post_data = (
            instance.accounting_opinion_submitted_by_post
        )
        approved_by_post_data = instance.approved_by_post

        representation["project"] = self.get_project_data(project) if project else None
        representation["estimated_by"] = (
            self.get_employee_data(estimated_by_data) if estimated_by_data else None
        )
        representation["cited_by"] = (
            self.get_employee_data(cited_by_data) if cited_by_data else None
        )
        representation["recommended_by"] = (
            self.get_employee_data(recommended_by_data) if recommended_by_data else None
        )
        representation["accounting_opinion_submitted_by"] = (
            self.get_employee_data(accounting_opinion_submitted_by_data)
            if accounting_opinion_submitted_by_data
            else None
        )
        representation["approved_by"] = (
            self.get_employee_data(approved_by_data) if approved_by_data else None
        )
        representation["estimated_by_post"] = (
            self.get_position_data(estimated_by_post_data)
            if estimated_by_post_data
            else None
        )
        representation["cited_by_post"] = (
            self.get_position_data(cited_by_post_data) if cited_by_post_data else None
        )
        representation["recommended_by_post"] = (
            self.get_position_data(recommended_by_post_data)
            if recommended_by_post_data
            else None
        )
        representation["accounting_opinion_submitted_by_post"] = (
            self.get_position_data(accounting_opinion_submitted_by_post_data)
            if accounting_opinion_submitted_by_post_data
            else None
        )
        representation["approved_by_post"] = (
            self.get_position_data(approved_by_post_data)
            if approved_by_post_data
            else None
        )
        return representation

    def get_employee_data(self, data):
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            full_name_eng: full_name_eng,
        }

    def get_position_data(self, data):
        return {"id": data.id, "name": data.name, "name_eng": str(data.name_eng)}

    def get_project_data(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
        }


class TenderSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    bids_purchase_branch = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )
    bids_enrollment_branch = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )
    contact_branch = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )
    new_paper_name = serializers.PrimaryKeyRelatedField(
        queryset=NewsPaper.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectTender
        fields = (
            "id",
            "project",
            "first_published_date",
            "first_published_date_eng",
            "bids_purchase_last_date",
            "bids_purchase_last_date_eng",
            "bids_purchase_time",
            "bids_enrollment_last_date",
            "bids_enrollment_last_date_eng",
            "bids_enrollment_time",
            "bids_open_date",
            "bids_open_date_eng",
            "bids_open_time",
            "bids_purchase_branch",
            "bids_enrollment_branch",
            "contact_branch",
            "invoice_date",
            "invoice_date_eng",
            "invoice_no",
            "new_paper_name",
            "news_paper_address",
            "printing_press",
            "paper_page_no",
            "info_publication_no",
            "info_publication_price",
            "publication_date",
            "publication_date_eng",
            "voucher_date",
            "voucher_date_eng",
            "voucher_no",
            "address1",
            "address2",
            "address3",
            "address4",
            "address5",
            "address6",
            "representative_invoice_date",
            "representative_invoice_date_eng",
            "representative_invoice_no",
            "representative_send_date",
            "representative_send_time",
            "representative_send_address",
            "representative1",
            "representative2",
            "representative3",
            "representative4",
            "representative5",
            "representative6",
            "print_custom_report",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "first_published_date": {"required": False, "allow_null": True},
            "first_published_date_eng": {"required": False, "allow_null": True},
            "bids_purchase_last_date": {"required": False, "allow_null": True},
            "bids_purchase_last_date_eng": {"required": False, "allow_null": True},
            "bids_purchase_time": {"required": False, "allow_null": True},
            "bids_enrollment_last_date": {"required": False, "allow_null": True},
            "bids_enrollment_last_date_eng": {"required": False, "allow_null": True},
            "bids_enrollment_time": {"required": False, "allow_null": True},
            "bids_open_date": {"required": False, "allow_null": True},
            "bids_open_date_eng": {"required": False, "allow_null": True},
            "bids_open_time": {"required": False, "allow_null": True},
            "bids_purchase_branch": {"required": False, "allow_null": True},
            "bids_enrollment_branch": {"required": False, "allow_null": True},
            "contact_branch": {"required": False, "allow_null": True},
            "invoice_date": {"required": False, "allow_null": True},
            "invoice_date_eng": {"required": False, "allow_null": True},
            "invoice_no": {"required": False, "allow_null": True},
            "new_paper_name": {"required": False, "allow_null": True},
            "news_paper_address": {"required": False, "allow_null": True},
            "printing_press": {"required": False, "allow_null": True},
            "paper_page_no": {"required": False, "allow_null": True},
            "info_publication_no": {"required": False, "allow_null": True},
            "info_publication_price": {"required": False, "allow_null": True},
            "publication_date": {"required": False, "allow_null": True},
            "publication_date_eng": {"required": False, "allow_null": True},
            "voucher_date": {"required": False, "allow_null": True},
            "voucher_date_eng": {"required": False, "allow_null": True},
            "voucher_no": {"required": False, "allow_null": True},
            "address1": {"required": False, "allow_null": True},
            "address2": {"required": False, "allow_null": True},
            "address3": {"required": False, "allow_null": True},
            "address4": {"required": False, "allow_null": True},
            "address5": {"required": False, "allow_null": True},
            "address6": {"required": False, "allow_null": True},
            "representative_invoice_date": {"required": False, "allow_null": True},
            "representative_invoice_date_eng": {"required": False, "allow_null": True},
            "representative_invoice_no": {"required": False, "allow_null": True},
            "representative_send_date": {"required": False, "allow_null": True},
            "representative_send_time": {"required": False, "allow_null": True},
            "representative_send_address": {"required": False, "allow_null": True},
            "representative1": {"required": False, "allow_null": True},
            "representative2": {"required": False, "allow_null": True},
            "representative3": {"required": False, "allow_null": True},
            "representative4": {"required": False, "allow_null": True},
            "representative5": {"required": False, "allow_null": True},
            "representative6": {"required": False, "allow_null": True},
            "print_custom_report": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        bids_purchase_branch = instance.bids_purchase_branch
        bids_enrollment_branch = instance.bids_enrollment_branch
        contact_branch = instance.contact_branch
        new_paper_name = instance.new_paper_name

        representation["project"] = self.get_common_data(project) if project else None
        representation["bids_purchase_branch"] = (
            self.get_common_data(bids_purchase_branch) if bids_purchase_branch else None
        )
        representation["bids_enrollment_branch"] = (
            self.get_common_data(bids_enrollment_branch)
            if bids_enrollment_branch
            else None
        )
        representation["contact_branch"] = (
            self.get_common_data(contact_branch) if contact_branch else None
        )
        representation["new_paper_name"] = (
            self.get_common_data(new_paper_name) if new_paper_name else None
        )
        return representation


class ProjectBidCollectionSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    builder = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False, allow_null=True
    )
    bank = serializers.PrimaryKeyRelatedField(
        queryset=BFI.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectBidCollection
        fields = (
            "id",
            "project",
            "builder",
            "is_legal",
            "bail_type",
            "bail_amount",
            "bank",
            "bank_guarantee_no",
            "start_date",
            "start_date_eng",
            "end_date",
            "end_date_eng",
            "bank_guarantee_type",
            "total_amount",
            "mu_aa_ka",
            "total",
            "is_approved",
            "attached_documents_list",
            "remark",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "builder": {"required": False, "allow_null": True},
            "is_legal": {"required": False, "allow_null": True},
            "bail_type": {"required": False, "allow_null": True},
            "bail_amount": {"required": False, "allow_null": True},
            "bank": {"required": False, "allow_null": True},
            "bank_guarantee_no": {"required": False, "allow_null": True},
            "start_date": {"required": False, "allow_null": True},
            "start_date_eng": {"required": False, "allow_null": True},
            "end_date": {"required": False, "allow_null": True},
            "end_date_eng": {"required": False, "allow_null": True},
            "bank_guarantee_type": {"required": False, "allow_null": True},
            "total_amount": {"required": False, "allow_null": True},
            "mu_aa_ka": {"required": False, "allow_null": True},
            "total": {"required": False, "allow_null": True},
            "is_approved": {"required": False, "allow_null": True},
            "attached_documents_list": {"required": False, "allow_null": True},
            "remark": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        bank = instance.bank
        builder = instance.builder

        # representation["bail_type"] = instance.get_bail_type_display()
        # representation[
        #     "bank_guarantee_type"
        # ] = instance.get_bank_guarantee_type_display()
        representation["project"] = self.get_common_data(project) if project else None
        representation["bank"] = self.get_bank_data(bank) if bank else None
        representation["builder"] = self.org_data(builder) if builder else None
        return representation

    def org_data(self, data):
        return {
            "id": data.id,
            "full_name": data.full_name,
            "full_name_eng": data.full_name_eng,
        }


class ProjectDarbhauBidSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    firm = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectDarbhauBid
        fields = (
            "id",
            "project",
            "bid_sale_no",
            "bid_enrollment_no",
            "legal_bid",
            "comment_date",
            "comment_date_eng",
            "comment_no",
            "comment_approved_date",
            "comment_approved_date_eng",
            "position",
            "approved_by",
            "firm",
            "proprietor_name",
            "submitter_opinion",
            "accountant_opinion",
            "project_head_opinion",
            "office_head_decision",
            "executive_decision",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "bid_sale_no": {"required": False, "allow_null": True},
            "bid_enrollment_no": {"required": False, "allow_null": True},
            "legal_bid": {"required": False, "allow_null": True},
            "comment_date": {"required": False, "allow_null": True},
            "comment_date_eng": {"required": False, "allow_null": True},
            "comment_no": {"required": False, "allow_null": True},
            "comment_approved_date": {"required": False, "allow_null": True},
            "comment_approved_date_eng": {"required": False, "allow_null": True},
            "position": {"required": False, "allow_null": True},
            "approved_by": {"required": False, "allow_null": True},
            "firm": {"required": False, "allow_null": True},
            "proprietor_name": {"required": False, "allow_null": True},
            "submitter_opinion": {"required": False, "allow_null": True},
            "accountant_opinion": {"required": False, "allow_null": True},
            "project_head_opinion": {"required": False, "allow_null": True},
            "office_head_decision": {"required": False, "allow_null": True},
            "executive_decision": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        position = instance.position
        approved_by = instance.approved_by
        firm = instance.firm
        representation["project"] = self.get_common_data(project) if project else None
        representation["position"] = (
            self.get_common_data(position) if position else None
        )
        representation["approved_by"] = (
            self.employee_data(approved_by) if approved_by else None
        )
        representation["firm"] = self.firm_data(firm) if firm else None
        return representation

    def firm_data(self, data):
        return {
            "id": data.id,
            "full_name": data.full_name,
            "full_name_eng": data.full_name_eng,
            "registration_no": data.register_no,
        }

    def employee_data(self, data):
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            "full_name_eng": full_name_eng,
        }


class ProjectAgreementSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    firm_name = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False, allow_null=True
    )
    bank = serializers.PrimaryKeyRelatedField(
        queryset=BFI.objects.all(), required=False, allow_null=True
    )
    cw_position = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), required=False, allow_null=True
    )
    office_witness_1 = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    office_witness_1_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    office_witness_2 = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    office_witness_2_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    office_witness_3 = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    office_witness_3_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    office_witness_4 = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    office_witness_4_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectAgreement
        fields = (
            "id",
            "project",
            "contractor_invoiced_date",
            "contractor_invoiced_date_eng",
            "contractor_invoiced_no",
            "contractor_remarks_1",
            "contractor_remarks_2",
            "required_bail_amount",
            "required_performance_bond_amount",
            "required_bail_date",
            "required_bail_date_eng",
            "firm_name",
            "firm_address",
            "firm_contact_no",
            "grand_father_name",
            "father_name",
            "contracting_party_name",
            "age",
            "address",
            "contract_date",
            "contract_date_eng",
            "work_finished_date",
            "work_finished_date_eng",
            "exist_bail_amount",
            "exist_performance_bond_amount",
            "exist_bail_date",
            "exist_bail_date_eng",
            "bank",
            "exist_bank_guarantee_no",
            "end_date",
            "end_date_eng",
            "contractors_witness",
            "cw_position",
            "office_witness_1",
            "office_witness_1_position",
            "office_witness_2",
            "office_witness_2_position",
            "office_witness_3",
            "office_witness_3_position",
            "office_witness_4",
            "office_witness_4_position",
            "mandate_invoice_date",
            "mandate_invoice_date_eng",
            "mandate_invoice_no",
            "pa_sa",
            "remark_1",
            "remark_2",
            "remark_3",
            "remark_4",
            "officer_name",
            "officer_position",
            "print_custom_name",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "contractor_invoiced_date": {"required": False, "allow_null": True},
            "contractor_invoiced_date_eng": {"required": False, "allow_null": True},
            "contractor_invoiced_no": {"required": False, "allow_null": True},
            "contractor_remarks_1": {"required": False, "allow_null": True},
            "contractor_remarks_2": {"required": False, "allow_null": True},
            "required_bail_amount": {"required": False, "allow_null": True},
            "required_performance_bond_amount": {"required": False, "allow_null": True},
            "required_bail_date": {"required": False, "allow_null": True},
            "required_bail_date_eng": {"required": False, "allow_null": True},
            "firm_name": {"required": False, "allow_null": True},
            "firm_address": {"required": False, "allow_null": True},
            "firm_contact_no": {"required": False, "allow_null": True},
            "grand_father_name": {"required": False, "allow_null": True},
            "father_name": {"required": False, "allow_null": True},
            "contracting_party_name": {"required": False, "allow_null": True},
            "age": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
            "contract_date": {"required": False, "allow_null": True},
            "contract_date_eng": {"required": False, "allow_null": True},
            "work_finished_date": {"required": False, "allow_null": True},
            "work_finished_date_eng": {"required": False, "allow_null": True},
            "exist_bail_amount": {"required": False, "allow_null": True},
            "exist_performance_bond_amount": {"required": False, "allow_null": True},
            "exist_bail_date": {"required": False, "allow_null": True},
            "exist_bail_date_eng": {"required": False, "allow_null": True},
            "bank": {"required": False, "allow_null": True},
            "exist_bank_guarantee_no": {"required": False, "allow_null": True},
            "end_date": {"required": False, "allow_null": True},
            "end_date_eng": {"required": False, "allow_null": True},
            "contractors_witness": {"required": False, "allow_null": True},
            "cw_position": {"required": False, "allow_null": True},
            "office_witness_1": {"required": False, "allow_null": True},
            "office_witness_1_position": {"required": False, "allow_null": True},
            "office_witness_2": {"required": False, "allow_null": True},
            "office_witness_2_position": {"required": False, "allow_null": True},
            "office_witness_3": {"required": False, "allow_null": True},
            "office_witness_3_position": {"required": False, "allow_null": True},
            "office_witness_4": {"required": False, "allow_null": True},
            "office_witness_4_position": {"required": False, "allow_null": True},
            "mandate_invoice_date": {"required": False, "allow_null": True},
            "mandate_invoice_date_eng": {"required": False, "allow_null": True},
            "mandate_invoice_no": {"required": False, "allow_null": True},
            "pa_sa": {"required": False, "allow_null": True},
            "remark_1": {"required": False, "allow_null": True},
            "remark_2": {"required": False, "allow_null": True},
            "remark_3": {"required": False, "allow_null": True},
            "remark_4": {"required": False, "allow_null": True},
            "officer_name": {"required": False, "allow_null": True},
            "officer_position": {"required": False, "allow_null": True},
            "print_custom_name": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        firm_name = instance.firm_name
        bank = instance.bank
        cw_position = instance.cw_position
        office_witness_1 = instance.office_witness_1
        office_witness_1_position = instance.office_witness_1_position
        office_witness_2 = instance.office_witness_2
        office_witness_2_position = instance.office_witness_2_position
        office_witness_3 = instance.office_witness_3
        office_witness_3_position = instance.office_witness_3_position
        office_witness_4 = instance.office_witness_4
        office_witness_4_position = instance.office_witness_4_position
        representation["project"] = self.get_common_data(project) if project else None
        representation["firm_name"] = (
            self.get_firm_data(firm_name) if firm_name else None
        )
        representation["bank"] = self.get_bank_data(bank) if bank else None
        representation["cw_position"] = (
            self.get_common_data(cw_position) if cw_position else None
        )
        representation["office_witness_1"] = (
            self.employee_data(office_witness_1) if office_witness_1 else None
        )
        representation["office_witness_1_position"] = (
            self.get_common_data(office_witness_1_position)
            if office_witness_1_position
            else None
        )
        representation["office_witness_2"] = (
            self.employee_data(office_witness_2) if office_witness_2 else None
        )
        representation["office_witness_2_position"] = (
            self.get_common_data(office_witness_2_position)
            if office_witness_2_position
            else None
        )
        representation["office_witness_3"] = (
            self.employee_data(office_witness_3) if office_witness_3 else None
        )
        representation["office_witness_3_position"] = (
            self.get_common_data(office_witness_3_position)
            if office_witness_3_position
            else None
        )
        representation["office_witness_4"] = (
            self.employee_data(office_witness_4) if office_witness_4 else None
        )
        representation["office_witness_4_position"] = (
            self.get_common_data(office_witness_4_position)
            if office_witness_4_position
            else None
        )
        return representation

    def employee_data(self, data):
        if not data:
            return {}
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            full_name_eng: full_name_eng,
        }

    def get_firm_data(self, data):
        if not data:
            return {}
        return {
            "id": data.id,
            "full_name": data.full_name,
            "full_name_eng": data.full_name_eng,
            "register_no": data.register_no,
        }


class ProjectMobilizationDetailSerializer(PlanExecutionBaseSerializer):
    mobilization = serializers.PrimaryKeyRelatedField(
        queryset=ProjectMobilization.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    institution = serializers.PrimaryKeyRelatedField(
        queryset=SourceReceipt.objects.all(), required=False, allow_null=True
    )
    accounting_topic = serializers.PrimaryKeyRelatedField(
        queryset=AccountTitleManagement.objects.all(), required=False, allow_null=True
    )
    budget_source = serializers.PrimaryKeyRelatedField(
        queryset=BudgetSource.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectMobilizationDetail
        fields = (
            "id",
            "mobilization",
            "institution",
            "accounting_topic",
            "budget_source",
            "percentage",
            "amount",
            "remarks",
        )
        extra_kwargs = {
            "mobilization": {"required": False, "allow_null": True},
            "institution": {"required": False, "allow_null": True},
            "accounting_topic": {"required": False, "allow_null": True},
            "budget_source": {"required": False, "allow_null": True},
            "percentage": {"required": False, "allow_null": True},
            "amount": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        institution = instance.institution
        accounting_topic = instance.accounting_topic
        budget_source = instance.budget_source
        representation["institution"] = (
            self.get_common_data(institution) if institution else None
        )
        representation["accounting_topic"] = (
            self.get_common_data(accounting_topic) if accounting_topic else None
        )
        representation["budget_source"] = (
            self.get_common_data(budget_source) if budget_source else None
        )
        return representation


class ProjectMobilizationSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    mobilization_details = ProjectMobilizationDetailSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = ProjectMobilization
        fields = (
            "id",
            "project",
            "date",
            "date_eng",
            "comment_no",
            "project_amount",
            "percent",
            "mobilization_amount",
            "address",
            "remarks",
            "print_custom_report",
            "mobilization_details",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "date": {"required": False, "allow_null": True},
            "date_eng": {"required": False, "allow_null": True},
            "comment_no": {"required": False, "allow_null": True},
            "project_amount": {"required": False, "allow_null": True},
            "percent": {"required": False, "allow_null": True},
            "mobilization_amount": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "print_custom_report": {"required": False, "allow_null": True},
            "mobilization_details": {"required": False, "allow_null": True},
        }


class PaymentDetailSerializer(PlanExecutionBaseSerializer):
    expense_topic = serializers.PrimaryKeyRelatedField(
        queryset=AccountTitleManagement.objects.all(), required=False, allow_null=True
    )
    source = serializers.PrimaryKeyRelatedField(
        queryset=SourceReceipt.objects.all(), required=False, allow_null=True
    )
    subject_work_area = serializers.PrimaryKeyRelatedField(
        queryset=SubjectArea.objects.all(), required=False, allow_null=True
    )
    payment_type = serializers.PrimaryKeyRelatedField(
        queryset=CollectPayment.objects.all(), required=False, allow_null=True
    )
    peb = serializers.PrimaryKeyRelatedField(
        queryset=PaymentExitBill.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = PaymentDetail
        fields = (
            "id",
            "expense_topic",
            "source",
            "subject_work_area",
            "payment_type",
            "amount",
            "remarks",
            "peb",
        )
        extra_kwargs = {
            "expense_topic": {"required": False, "allow_null": True},
            "source": {"required": False, "allow_null": True},
            "subject_work_area": {"required": False, "allow_null": True},
            "payment_type": {"required": False, "allow_null": True},
            "amount": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "peb": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        expense_topic = instance.expense_topic
        source = instance.source
        subject_work_area = instance.subject_work_area
        payment_type = instance.payment_type
        representation["expense_topic"] = (
            self.get_common_data(expense_topic) if expense_topic else None
        )
        representation["source"] = self.get_common_data(source) if source else None
        representation["subject_work_area"] = (
            self.get_common_data(subject_work_area) if subject_work_area else None
        )
        representation["payment_type"] = (
            self.get_common_data(payment_type) if payment_type else None
        )
        return representation


class PaymentExitBillSerializer(PlanExecutionBaseSerializer):
    payment_details = PaymentDetailSerializer(many=True, read_only=True)
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    installment = serializers.PrimaryKeyRelatedField(
        queryset=ProjectInstallment.objects.all(),
        required=False,
        allow_null=True,
    )
    check_pass_name = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    check_pass_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    ready_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    ready_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    submitted_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    submitted_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    approved_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = PaymentExitBill
        fields = (
            "id",
            "payment_details",
            "letter_no",
            "cha_no",
            "project",
            "exit_date",
            "exit_date_eng",
            "installment",
            "u_sa_maag_amount",
            "payment_mode",
            "check_pass_date",
            "check_pass_date_eng",
            "check_pass_name",
            "check_pass_position",
            "disbursement_assessment_amount",
            "check_pass_amount",
            "contentment_amount",
            "mu_aa_ka",
            "marmat_sambhar_fund_amount",
            "env_disaster_fund_amount",
            "public_participation_percent",
            "public_participation_amount",
            "reinstatement_tex",
            "advance_income_tex",
            "withdrawal_eligible_amount",
            "remark",
            "ready_by",
            "plan_mst_total_amount",
            "nikasha_total_amount",
            "peski_amount",
            "total_remaining_amount",
            "ready_by_position",
            "submitted_by",
            "submitted_by_position",
            "approved_by",
            "approved_by_position",
            "status",
        )
        read_only_fields = (
            "plan_mst_total_amount",
            "nikasha_total_amount",
            "peski_amount",
            "total_remaining_amount",
        )
        extra_kwargs = {
            "payment_details": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "exit_date": {"required": False, "allow_null": True},
            "exit_date_eng": {"required": False, "allow_null": True},
            "installment": {"required": False, "allow_null": True},
            "u_sa_maag_amount": {"required": False, "allow_null": True},
            "check_pass_date": {"required": False, "allow_null": True},
            "check_pass_date_eng": {"required": False, "allow_null": True},
            "check_pass_name": {"required": False, "allow_null": True},
            "check_pass_position": {"required": False, "allow_null": True},
            "disbursement_assessment_amount": {"required": False, "allow_null": True},
            "check_pass_amount": {"required": False, "allow_null": True},
            "contentment_amount": {"required": False, "allow_null": True},
            "mu_aa_ka": {"required": False, "allow_null": True},
            "marmat_sambhar_fund_amount": {"required": False, "allow_null": True},
            "env_disaster_fund_amount": {"required": False, "allow_null": True},
            "public_participation_percent": {"required": False, "allow_null": True},
            "public_participation_amount": {"required": False, "allow_null": True},
            "reinstatement_tex": {"required": False, "allow_null": True},
            "advance_income_tex": {"required": False, "allow_null": True},
            "withdrawal_eligible_amount": {"required": False, "allow_null": True},
            "remark": {"required": False, "allow_null": True},
            "ready_by": {"required": False, "allow_null": True},
            "ready_by_position": {"required": False, "allow_null": True},
            "submitted_by": {"required": False, "allow_null": True},
            "submitted_by_position": {"required": False, "allow_null": True},
            "approved_by": {"required": False, "allow_null": True},
            "approved_by_position": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        installment = instance.installment
        check_pass_name = instance.check_pass_name
        check_pass_position = instance.check_pass_position
        ready_by = instance.ready_by
        ready_by_position = instance.ready_by_position
        submitted_by = instance.submitted_by
        submitted_by_position = instance.submitted_by_position
        approved_by = instance.approved_by
        approved_by_position = instance.approved_by_position

        representation["project"] = self.get_common_data(project) if project else None
        representation["installment"] = (
            self.get_common_data(installment) if installment else None
        )
        representation["check_pass_name"] = (
            self.employee_data(check_pass_name) if check_pass_name else None
        )
        representation["check_pass_position"] = (
            self.get_common_data(check_pass_position) if check_pass_position else None
        )
        representation["ready_by"] = self.employee_data(ready_by) if ready_by else None
        representation["ready_by_position"] = (
            self.get_common_data(ready_by_position) if ready_by_position else None
        )
        representation["submitted_by"] = (
            self.employee_data(submitted_by) if submitted_by else None
        )
        representation["submitted_by_position"] = (
            self.get_common_data(submitted_by_position)
            if submitted_by_position
            else None
        )
        representation["approved_by"] = (
            self.employee_data(approved_by) if approved_by else None
        )
        representation["approved_by_position"] = (
            self.get_common_data(approved_by_position) if approved_by_position else None
        )

        return representation

    def employee_data(self, data):
        if not data:
            return {}
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            full_name_eng: full_name_eng,
        }


class ProjectDeadlineSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    decision_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    site_inspector = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    site_inspector_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectDeadline
        fields = (
            "id",
            "project",
            "cha_no",
            "letter_no",
            "deadline_date",
            "deadline_date_eng",
            "decision_date",
            "decision_date_eng",
            "decision_by",
            "site_inspector",
            "site_inspector_position",
            "site_inspection_date",
            "reason",
            "remark",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "deadline_date": {"required": False, "allow_null": True},
            "deadline_date_eng": {"required": False, "allow_null": True},
            "decision_date": {"required": False, "allow_null": True},
            "decision_date_eng": {"required": False, "allow_null": True},
            "decision_by": {"required": False, "allow_null": True},
            "reason": {"required": False, "allow_null": True},
            "remark": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["project"] = self.get_common_data(instance.project)
        data["decision_by"] = self.employee_data(instance.decision_by)
        data["site_inspector"] = self.employee_data(instance.site_inspector)
        data["site_inspector_position"] = self.get_common_data(
            instance.site_inspector_position
        )
        return data


class MeasuringBookSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    activity = serializers.PrimaryKeyRelatedField(
        queryset=ProjectActivity.objects.all(), required=False, allow_null=True
    )
    contractor = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False, allow_null=True
    )
    contractor_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    measured_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    measured_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    checked_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    checked_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    approved_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = MeasuringBook
        fields = (
            "id",
            "project",
            "measuring_no",
            "activity",
            "page_no",
            "measuring_date",
            "measuring_date_eng",
            "total_amount",
            "previous_measuring_book_amount",
            "this_measuring_book_amount",
            "result_obtained_so_far",
            "rate_in_list",
            "length",
            "breath",
            "height",
            "contractor",
            "contractor_position",
            "measured_by",
            "measured_by_position",
            "checked_by",
            "checked_by_position",
            "approved_by",
            "approved_by_position",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "measuring_no": {"required": False, "allow_null": True},
            "activity": {"required": False, "allow_null": True},
            "page_no": {"required": False, "allow_null": True},
            "measuring_date": {"required": False, "allow_null": True},
            "measuring_date_eng": {"required": False, "allow_null": True},
            "total_amount": {"required": False, "allow_null": True},
            "previous_measuring_book_amount": {"required": False, "allow_null": True},
            "this_measuring_book_amount": {"required": False, "allow_null": True},
            "result_obtained_so_far": {"required": False, "allow_null": True},
            "rate_in_list": {"required": False, "allow_null": True},
            "length": {"required": False, "allow_null": True},
            "breath": {"required": False, "allow_null": True},
            "height": {"required": False, "allow_null": True},
            "contractor": {"required": False, "allow_null": True},
            "contractor_position": {"required": False, "allow_null": True},
            "measured_by": {"required": False, "allow_null": True},
            "measured_by_position": {"required": False, "allow_null": True},
            "checked_by": {"required": False, "allow_null": True},
            "checked_by_position": {"required": False, "allow_null": True},
            "approved_by": {"required": False, "allow_null": True},
            "approved_by_position": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        activity = instance.activity
        contractor = instance.contractor
        contractor_position = instance.contractor_position
        measured_by = instance.measured_by
        measured_by_position = instance.measured_by_position
        checked_by = instance.checked_by
        checked_by_position = instance.checked_by_position
        approved_by = instance.approved_by
        approved_by_position = instance.approved_by_position

        representation["project"] = self.get_common_data(project)
        representation["activity"] = self.get_common_data(activity)
        representation["contractor"] = self.get_common_data(contractor)
        representation["contractor_position"] = self.get_common_data(
            contractor_position
        )
        representation["measured_by"] = self.employee_data(measured_by)
        representation["measured_by_position"] = self.get_common_data(
            measured_by_position
        )
        representation["checked_by"] = self.employee_data(checked_by)
        representation["checked_by_position"] = self.get_common_data(
            checked_by_position
        )
        representation["approved_by"] = self.employee_data(approved_by)
        representation["approved_by_position"] = self.get_common_data(
            approved_by_position
        )
        return representation

    def employee_data(self, data):
        if not data:
            return {}
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            full_name_eng: full_name_eng,
        }


class ProjectFinishedBailReturnSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    approved_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectFinishedBailReturn
        fields = (
            "id",
            "project",
            "comment_no",
            "date",
            "date_eng",
            "executive_decision",
            "approved_by",
            "approved_by_position",
            "print_custom_report",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "comment_no": {"required": False, "allow_null": True},
            "date": {"required": False, "allow_null": True},
            "date_eng": {"required": False, "allow_null": True},
            "executive_decision": {"required": False, "allow_null": True},
            "approved_by": {"required": False, "allow_null": True},
            "approved_by_position": {"required": False, "allow_null": True},
            "print_custom_report": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        approved_by = instance.approved_by
        representation["project"] = self.get_common_data(project) if project else None
        representation["approved_by"] = (
            self.employee_data(approved_by) if approved_by else None
        )
        representation["approved_by_position"] = EmployeeSectorSerializer(
            instance.approved_by_position
        ).data
        return representation

    def employee_data(self, data):
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            "full_name_eng": full_name_eng,
        }


class ConsumerFormulationSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    emp_name = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    consumer_committee = serializers.PrimaryKeyRelatedField(
        queryset=ConsumerCommittee.objects.all(), required=False, allow_null=True
    )
    selected_consumer_committee = serializers.PrimaryKeyRelatedField(
        queryset=ConsumerCommittee.objects.all(), required=False, allow_null=True
    )
    monitoring_committee = serializers.PrimaryKeyRelatedField(
        queryset=MonitoringCommittee.objects.all(), required=False, allow_null=True
    )
    monitor_committee = MonitoringCommitteeMemberSerializer(many=True)

    class Meta:
        model = ConsumerFormulation
        fields = (
            "id",
            "project",
            "print_custom_report",
            "first_time_publish",
            "first_time_publish_eng",
            "form_amount",
            "consumer_committee",
            "consumer_committee_name",
            "selected_consumer_committee",
            "code",
            "chairman",
            "address",
            "established_date",
            "phone",
            "report_date",
            "report_date_eng",
            "invoice_no",
            "project_current_status",
            "previous_work",
            "detail_from_office_date",
            "detail_from_office_date_eng",
            "office_lecture",
            "emp_name",
            "position",
            "opinion",
            "positive_effect",
            "other",
            "project_related_other",
            "monitoring_committee",
            "monitor_committee",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "print_custom_report": {"required": False, "allow_null": True},
            "first_time_publish": {"required": False, "allow_null": True},
            "first_time_publish_eng": {"required": False, "allow_null": True},
            "form_amount": {"required": False, "allow_null": True},
            "consumer_committee": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "chairman": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
            "established_date": {"required": False, "allow_null": True},
            "phone": {"required": False, "allow_null": True},
            "report_date": {"required": False, "allow_null": True},
            "report_date_eng": {"required": False, "allow_null": True},
            "invoice_no": {"required": False, "allow_null": True},
            "project_current_status": {"required": False, "allow_null": True},
            "previous_work": {"required": False, "allow_null": True},
            "detail_from_office_date": {"required": False, "allow_null": True},
            "detail_from_office_date_eng": {"required": False, "allow_null": True},
            "office_lecture": {"required": False, "allow_null": True},
            "emp_name": {"required": False, "allow_null": True},
            "position": {"required": False, "allow_null": True},
            "opinion": {"required": False, "allow_null": True},
            "positive_effect": {"required": False, "allow_null": True},
            "other": {"required": False, "allow_null": True},
            "project_related_other": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        consumer_committee = instance.consumer_committee
        selected_consumer_committee = instance.selected_consumer_committee
        emp_name = instance.emp_name
        position = instance.position

        representation["project"] = self.get_common_data(project) if project else None
        representation["consumer_committee"] = (
            self.consumer_committee_data(consumer_committee)
            if consumer_committee
            else None
        )
        representation["selected_consumer_committee"] = (
            self.consumer_committee_data(selected_consumer_committee)
            if selected_consumer_committee
            else None
        )
        representation["emp_name"] = self.emp_data(emp_name) if emp_name else None
        representation["position"] = (
            self.get_common_data(position) if position else None
        )
        return representation

    def emp_data(self, data):
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            "full_name_eng": full_name_eng,
        }

    def consumer_committee_data(self, data):
        return {
            "id": data.id,
            "code": data.code,
            "full_name": data.full_name,
            "full_name_eng": data.full_name_eng,
            "registration_no": data.registration_no,
        }


class PSABuildingMaterialSerializer(PlanExecutionBaseSerializer):
    material = serializers.PrimaryKeyRelatedField(
        queryset=ConstructionMaterialDescription.objects.all(),
        required=False,
        allow_null=True,
    )
    probability_study_approve = serializers.PrimaryKeyRelatedField(
        queryset=ProbabilityStudyApprove.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = BuildingMaterialDetail
        fields = (
            "probability_study_approve",
            "id",
            "material",
            "amount",
            "rupees",
            "remark",
            "status",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        source_data = instance.source
        material_data = instance.material
        representation["source"] = (
            self.get_source_data(source_data) if source_data else None
        )
        representation["material"] = (
            self.get_common_data(material_data) if material_data else None
        )
        return representation

    def get_source_data(self, data):
        return {
            "phone_number": data.phone_number,
            "email": data.email,
            "country": data.country,
            "address": data.address,
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
        }


class ProbabilityStudyApproveSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    project_selection = serializers.PrimaryKeyRelatedField(
        queryset=SelectionFeasibility.objects.all(), required=False, allow_null=True
    )
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    approved_date_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    to_approve_submission_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    to_approve_submission_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    to_approve_check_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    to_approve_check_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    to_approve_recommendation_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    to_approve_recommendation_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    to_approve_approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    to_approve_approved_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    check_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    check_date_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    recommendation_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    recommendation_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    materials = PSABuildingMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = ProbabilityStudyApprove
        fields = (
            "id",
            "project",
            "project_selection",
            "consumer_benefits",
            "engineer_survey_to_start_future",
            "recommender_opinion",
            "approvers_opinion",
            "approved_amount_percent",
            "decision",
            "submission_date",
            "submission_date_eng",
            "submission_date_by",
            "submission_date_by_position",
            "check_date",
            "check_date_eng",
            "check_by",
            "check_date_by_position",
            "recommendation_date",
            "recommendation_date_eng",
            "recommendation_by",
            "recommendation_by_position",
            "approved_date",
            "approved_date_eng",
            "materials",
            "approved_by",
            "approved_date_by_position",
            "to_approve_submission_date",
            "to_approve_submission_date_eng",
            "to_approve_submission_by",
            "to_approve_submission_by_position",
            "to_approve_check_date",
            "to_approve_check_date_eng",
            "to_approve_check_by",
            "to_approve_check_by_position",
            "to_approve_recommendation_date",
            "to_approve_recommendation_date_eng",
            "to_approve_recommendation_by",
            "to_approve_recommendation_by_position",
            "to_approve_approved_date",
            "to_approve_approved_date_eng",
            "to_approve_approved_by",
            "to_approve_approved_by_position",
            "invoice_no",
            "label",
            "pa_na",
            "final_report_approved_by",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "project_selection": {"required": False, "allow_null": True},
            "consumer_benefits": {"required": False, "allow_null": True},
            "engineer_survey_to_start_future": {"required": False, "allow_null": True},
            "recommender_opinion": {"required": False, "allow_null": True},
            "approvers_opinion": {"required": False, "allow_null": True},
            "approved_amount_percent": {"required": False, "allow_null": True},
            "decision": {"required": False, "allow_null": True},
            "submission_date": {"required": False, "allow_null": True},
            "submission_date_eng": {"required": False, "allow_null": True},
            "submission_date_by": {"required": False, "allow_null": True},
            "submission_date_by_position": {"required": False, "allow_null": True},
            "check_date": {"required": False, "allow_null": True},
            "check_date_eng": {"required": False, "allow_null": True},
            "check_by": {"required": False, "allow_null": True},
            "check_date_by_position": {"required": False, "allow_null": True},
            "recommendation_date": {"required": False, "allow_null": True},
            "recommendation_date_eng": {"required": False, "allow_null": True},
            "recommendation_by": {"required": False, "allow_null": True},
            "recommendation_by_position": {"required": False, "allow_null": True},
            "approved_date": {"required": False, "allow_null": True},
            "approved_date_eng": {"required": False, "allow_null": True},
            "approved_by": {"required": False, "allow_null": True},
            "approved_date_by_position": {"required": False, "allow_null": True},
            "to_approve_submission_date": {"required": False, "allow_null": True},
            "to_approve_submission_date_eng": {"required": False, "allow_null": True},
            "to_approve_submission_by": {"required": False, "allow_null": True},
            "to_approve_submission_by_position": {
                "required": False,
                "allow_null": True,
            },
            "to_approve_check_date": {"required": False, "allow_null": True},
            "to_approve_check_date_eng": {"required": False, "allow_null": True},
            "to_approve_check_by": {"required": False, "allow_null": True},
            "to_approve_check_by_position": {"required": False, "allow_null": True},
            "to_approve_recommendation_date": {"required": False, "allow_null": True},
            "to_approve_recommendation_date_eng": {
                "required": False,
                "allow_null": True,
            },
            "to_approve_recommendation_by": {"required": False, "allow_null": True},
            "to_approve_recommendation_by_position": {
                "required": False,
                "allow_null": True,
            },
            "to_approve_approved_date": {"required": False, "allow_null": True},
            "to_approve_approved_date_eng": {"required": False, "allow_null": True},
            "to_approve_approved_by": {"required": False, "allow_null": True},
            "to_approve_approved_by_position": {"required": False, "allow_null": True},
            "invoice_no": {"required": False, "allow_null": True},
            "label": {"required": False, "allow_null": True},
            "pa_na": {"required": False, "allow_null": True},
            "final_report_approved_by": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        project_selection = instance.project_selection
        approved_by = instance.approved_by
        approved_date_by_position = instance.approved_date_by_position
        to_approve_submission_by = instance.to_approve_submission_by
        to_approve_submission_by_position = instance.to_approve_submission_by_position
        to_approve_check_by = instance.to_approve_check_by
        to_approve_check_by_position = instance.to_approve_check_by_position
        to_approve_recommendation_by = instance.to_approve_recommendation_by
        to_approve_recommendation_by_position = (
            instance.to_approve_recommendation_by_position
        )
        to_approve_approved_by = instance.to_approve_approved_by
        to_approve_approved_by_position = instance.to_approve_approved_by_position
        check_by = instance.check_by
        check_date_by_position = instance.check_date_by_position
        recommendation_by = instance.recommendation_by
        recommendation_by_position = instance.recommendation_by_position

        representation["project"] = self.get_common_data(project) if project else None
        representation["project_selection"] = (
            self.get_common_data(project_selection) if project_selection else None
        )
        representation["approved_by"] = (
            self.emp_data(approved_by) if approved_by else None
        )
        representation["approved_date_by_position"] = (
            self.get_common_data(approved_date_by_position)
            if approved_date_by_position
            else None
        )
        representation["to_approve_submission_by"] = (
            self.emp_data(to_approve_submission_by)
            if to_approve_submission_by
            else None
        )
        representation["to_approve_submission_by_position"] = (
            self.get_common_data(to_approve_submission_by_position)
            if to_approve_submission_by_position
            else None
        )
        representation["to_approve_check_by"] = (
            self.emp_data(to_approve_check_by) if to_approve_check_by else None
        )
        representation["to_approve_check_by_position"] = (
            self.get_common_data(to_approve_check_by_position)
            if to_approve_check_by_position
            else None
        )
        representation["to_approve_recommendation_by"] = (
            self.emp_data(to_approve_recommendation_by)
            if to_approve_recommendation_by
            else None
        )
        representation["to_approve_recommendation_by_position"] = (
            self.get_common_data(to_approve_recommendation_by_position)
            if to_approve_recommendation_by_position
            else None
        )
        representation["to_approve_approved_by"] = (
            self.emp_data(to_approve_approved_by) if to_approve_approved_by else None
        )
        representation["to_approve_approved_by_position"] = (
            self.get_common_data(to_approve_approved_by_position)
            if to_approve_approved_by_position
            else None
        )
        representation["check_by"] = self.emp_data(check_by) if check_by else None
        representation["check_date_by_position"] = (
            self.get_common_data(check_date_by_position)
            if check_date_by_position
            else None
        )
        representation["recommendation_by"] = (
            self.emp_data(recommendation_by) if recommendation_by else None
        )
        representation["recommendation_by_position"] = (
            self.get_common_data(recommendation_by_position)
            if recommendation_by_position
            else None
        )
        return representation

    def emp_data(self, data):
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            "full_name_eng": full_name_eng,
        }


class InstallmentDetailSerializer(PlanExecutionBaseSerializer):
    installment = serializers.PrimaryKeyRelatedField(
        queryset=ProjectInstallment.objects.all(),
        required=False,
        allow_null=True,
    )
    opening_contract_account = serializers.PrimaryKeyRelatedField(
        queryset=OpeningContractAccount.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = InstallmentDetail
        fields = (
            "opening_contract_account",
            "id",
            "installment",
            "date",
            "date_eng",
            "nikasha_total_amount",
            "public_participation_percent",
            "remark",
            "status",
        )
        extra_kwargs = {
            "opening_contract_account": {"required": False, "allow_null": True},
            "installment": {"required": False, "allow_null": True},
            "date": {"required": False, "allow_null": True},
            "date_eng": {"required": False, "allow_null": True},
            "nikasha_total_amount": {"required": False, "allow_null": True},
            "public_participation_percent": {"required": False, "allow_null": True},
            "remark": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        installment = instance.installment
        representation["installment"] = (
            self.get_common_data(installment) if installment else None
        )
        return representation


class BuildingMaterialDetailSerializer(PlanExecutionBaseSerializer):
    source = serializers.PrimaryKeyRelatedField(
        queryset=BudgetSource.objects.all(), required=False, allow_null=True
    )
    material = serializers.PrimaryKeyRelatedField(
        queryset=ConstructionMaterialDescription.objects.all(),
        required=False,
        allow_null=True,
    )
    opening_contract_account = serializers.PrimaryKeyRelatedField(
        queryset=OpeningContractAccount.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = BuildingMaterialDetail
        fields = (
            "opening_contract_account",
            "id",
            "source",
            "material",
            "amount",
            "remark",
            "status",
        )
        extra_kwargs = {
            "opening_contract_account": {"required": False, "allow_null": True},
            "source": {"required": False, "allow_null": True},
            "material": {"required": False, "allow_null": True},
            "result": {"required": False, "allow_null": True},
            "remark": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        source_data = instance.source
        material_data = instance.material
        representation["source"] = (
            self.get_source_data(source_data) if source_data else None
        )
        representation["material"] = (
            self.get_common_data(material_data) if material_data else None
        )
        return representation

    def get_source_data(self, data):
        return {
            "phone_number": data.phone_number,
            "email": data.email,
            "country": data.country,
            "address": data.address,
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
        }


class MaintenanceArrangementSerializer(PlanExecutionBaseSerializer):
    opening_contract_account = serializers.PrimaryKeyRelatedField(
        queryset=OpeningContractAccount.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = MaintenanceArrangement
        fields = (
            "opening_contract_account",
            "id",
            "source",
            "amount",
            "remark",
            "status",
        )
        extra_kwargs = {
            "opening_contract_account": {"required": False, "allow_null": True},
            "source": {"required": False, "allow_null": True},
            "amount": {"required": False, "allow_null": True},
            "remark": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class OpeningContractAccountSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    bank_name = serializers.PrimaryKeyRelatedField(
        queryset=BFI.objects.all(), required=False, allow_null=True
    )
    witness_consumer_committee_post = serializers.PrimaryKeyRelatedField(
        queryset=ConsumerCommitteeMember.objects.all(), required=False, allow_null=True
    )
    secretary_of_consumer_committee_post = serializers.PrimaryKeyRelatedField(
        queryset=ConsumerCommitteeMember.objects.all(), required=False, allow_null=True
    )
    office_side_1 = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    office_side_1_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    office_side_2 = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    office_side_2_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    office_side_3 = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    office_side_3_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    office_side_4 = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    office_side_4_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all(), required=False, allow_null=True
    )
    installment = InstallmentDetailSerializer(many=True, read_only=True)
    materials = BuildingMaterialDetailSerializer(many=True, read_only=True)
    maintenance = MaintenanceArrangementSerializer(many=True, read_only=True)

    class Meta:
        model = OpeningContractAccount
        fields = (
            "id",
            "project",
            "cha_no",
            "pa_no",
            "date",
            "date_eng",
            "bank_name",
            "account_no",
            "bank_branch",
            "bodarth",
            "contract_ch_no",
            "contract_date",
            "contract_pa_no",
            "bodarth_1",
            "bodarth_2",
            "day",
            "contract_account_no",
            "print_custom_report",
            "project_contract_date",
            "project_contract_date_eng",
            "project_contract_start_date",
            "project_contract_start_date_eng",
            "project_completion_date",
            "project_completion_date_eng",
            "contract_no",
            "present_benefit",
            "absent_benefit",
            "project_start_experience",
            "other_experience",
            "cost_participation_subsidy",
            "public_service_labour_force",
            "arrangements_for_taking_care_of_repairs",
            "repairs_by_company",
            "committee_witness",
            "witness_consumer_committee_post",
            "user_committee_secretary",
            "secretary_of_consumer_committee_post",
            "office_side_1",
            "office_side_1_position",
            "office_side_2",
            "office_side_2_position",
            "office_side_3",
            "office_side_3_position",
            "office_side_4",
            "office_side_4_position",
            "mandate_ch_no",
            "mandate_date",
            "mandate_date_eng",
            "mandate_pa_no",
            "mandate_bodarth",
            "mandate_employee",
            "mandate_employee_position",
            "ward_no",
            "installment",
            "materials",
            "maintenance",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "cha_no": {"required": False, "allow_null": True},
            "pa_no": {"required": False, "allow_null": True},
            "date": {"required": False, "allow_null": True},
            "date_eng": {"required": False, "allow_null": True},
            "bank_name": {"required": False, "allow_null": True},
            "account_no": {"required": False, "allow_null": True},
            "bank_branch": {"required": False, "allow_null": True},
            "bodarth": {"required": False, "allow_null": True},
            "contract_ch_no": {"required": False, "allow_null": True},
            "contract_date": {"required": False, "allow_null": True},
            "contract_pa_no": {"required": False, "allow_null": True},
            "bodarth_1": {"required": False, "allow_null": True},
            "bodarth_2": {"required": False, "allow_null": True},
            "day": {"required": False, "allow_null": True},
            "contract_account_no": {"required": False, "allow_null": True},
            "print_custom_report": {"required": False, "allow_null": True},
            "project_contract_date": {"required": False, "allow_null": True},
            "project_contract_date_eng": {"required": False, "allow_null": True},
            "project_contract_start_date": {"required": False, "allow_null": True},
            "project_contract_start_date_eng": {"required": False, "allow_null": True},
            "project_completion_date": {"required": False, "allow_null": True},
            "project_completion_date_eng": {"required": False, "allow_null": True},
            "contract_no": {"required": False, "allow_null": True},
            "present_benefit": {"required": False, "allow_null": True},
            "absent_benefit": {"required": False, "allow_null": True},
            "project_start_experience": {"required": False, "allow_null": True},
            "other_experience": {"required": False, "allow_null": True},
            "arrangements_for_taking_care_of_repairs": {
                "required": False,
                "allow_null": True,
            },
            "repairs_by_company": {"required": False, "allow_null": True},
            "committee_witness": {"required": False, "allow_null": True},
            "user_committee_secretary": {"required": False, "allow_null": True},
            "office_side_1": {"required": False, "allow_null": True},
            "office_side_1_position": {"required": False, "allow_null": True},
            "office_side_2": {"required": False, "allow_null": True},
            "office_side_2_position": {"required": False, "allow_null": True},
            "office_side_3": {"required": False, "allow_null": True},
            "office_side_3_position": {"required": False, "allow_null": True},
            "office_side_4": {"required": False, "allow_null": True},
            "office_side_4_position": {"required": False, "allow_null": True},
            "mandate_ch_no": {"required": False, "allow_null": True},
            "mandate_date": {"required": False, "allow_null": True},
            "mandate_date_eng": {"required": False, "allow_null": True},
            "mandate_pa_no": {"required": False, "allow_null": True},
            "mandate_bodarth": {"required": False, "allow_null": True},
            "mandate_employee": {"required": False, "allow_null": True},
            "mandate_employee_position": {"required": False, "allow_null": True},
            "ward_no": {"required": False, "allow_null": True},
            "installment": {"required": False, "allow_null": True},
            "materials": {"required": False, "allow_null": True},
            "maintenance": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        bank_name = instance.bank_name

        witness_consumer_committee_post = instance.witness_consumer_committee_post
        secretary_of_consumer_committee_post = (
            instance.secretary_of_consumer_committee_post
        )

        office_side_1 = instance.office_side_1
        office_side_2 = instance.office_side_2
        office_side_3 = instance.office_side_3
        office_side_4 = instance.office_side_4

        office_side_1_position = instance.office_side_1_position
        office_side_2_position = instance.office_side_2_position
        office_side_3_position = instance.office_side_3_position
        office_side_4_position = instance.office_side_4_position

        representation["project"] = self.get_common_data(project) if project else None
        representation["bank_name"] = (
            self.get_bank_data(bank_name) if bank_name else None
        )
        representation["witness_consumer_committee_post"] = (
            self.get_common_data(witness_consumer_committee_post)
            if witness_consumer_committee_post
            else None
        )
        representation["secretary_of_consumer_committee_post"] = (
            self.get_common_data(secretary_of_consumer_committee_post)
            if secretary_of_consumer_committee_post
            else None
        )
        representation["office_side_1"] = (
            self.emp_data(office_side_1) if office_side_1 else None
        )
        representation["office_side_2"] = (
            self.emp_data(office_side_2) if office_side_2 else None
        )
        representation["office_side_3"] = (
            self.emp_data(office_side_3) if office_side_3 else None
        )
        representation["office_side_4"] = (
            self.emp_data(office_side_4) if office_side_4 else None
        )
        representation["office_side_1_position"] = (
            self.get_common_data(office_side_1_position)
            if office_side_1_position
            else None
        )
        representation["office_side_2_position"] = (
            self.get_common_data(office_side_2_position)
            if office_side_2_position
            else None
        )
        representation["office_side_3_position"] = (
            self.get_common_data(office_side_3_position)
            if office_side_3_position
            else None
        )
        representation["office_side_4_position"] = (
            self.get_common_data(office_side_4_position)
            if office_side_4_position
            else None
        )
        return representation

    def emp_data(self, data):
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            "full_name_eng": full_name_eng,
        }


class MonitoringCommitteeDetailSerializer(PlanExecutionBaseSerializer):
    member_type = serializers.PrimaryKeyRelatedField(
        queryset=MemberType.objects.all(),
        required=False,
        allow_null=True,
    )
    user_committee_monitoring = serializers.PrimaryKeyRelatedField(
        queryset=UserCommitteeMonitoring.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = MonitoringCommitteeDetail
        fields = (
            "id",
            "member_type",
            "member_position",
            "member_name",
            "phone_no",
            "present",
            "status",
            "user_committee_monitoring",
        )
        extra_kwargs = {
            "member_type": {"required": False, "allow_null": True},
            "member_position": {"required": False, "allow_null": True},
            "member_name": {"required": False, "allow_null": True},
            "phone_no": {"required": False, "allow_null": True},
            "present": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class UserCommitteeMonitoringSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    monitor_committee = MonitoringCommitteeMemberSerializer(many=True)

    class Meta:
        model = UserCommitteeMonitoring
        fields = (
            "id",
            "project",
            "project_amount",
            "assessment_amount",
            "amount_payable_as_per_assessment",
            "date",
            "date_eng",
            "meeting_address",
            "proposal_1",
            "proposal_2",
            "proposal_3",
            "print_custom_report",
            "monitor_committee",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "project_amount": {"required": False, "allow_null": True},
            "assessment_amount": {"required": False, "allow_null": True},
            "amount_payable_as_per_assessment": {"required": False, "allow_null": True},
            "date": {"required": False, "allow_null": True},
            "date_eng": {"required": False, "allow_null": True},
            "meeting_address": {"required": False, "allow_null": True},
            "proposal_1": {"required": False, "allow_null": True},
            "proposal_2": {"required": False, "allow_null": True},
            "proposal_3": {"required": False, "allow_null": True},
            "print_custom_report": {"required": False, "allow_null": True},
            "monitor_committee": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class ProjectRevisionSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    project_level = serializers.PrimaryKeyRelatedField(
        queryset=ProjectLevel.objects.all(), required=False, allow_null=True
    )
    project_type = serializers.PrimaryKeyRelatedField(
        queryset=ProjectType.objects.all(), required=False, allow_null=True
    )
    project_nature = serializers.PrimaryKeyRelatedField(
        queryset=ProjectNature.objects.all(), required=False, allow_null=True
    )
    work_class = serializers.PrimaryKeyRelatedField(
        queryset=WorkClass.objects.all(), required=False, allow_null=True
    )
    subject_area = serializers.PrimaryKeyRelatedField(
        queryset=SubjectArea.objects.all(), required=False, allow_null=True
    )
    strategic_sign = serializers.PrimaryKeyRelatedField(
        queryset=StrategicSign.objects.all(), required=False, allow_null=True
    )
    priority_type = serializers.PrimaryKeyRelatedField(
        queryset=PriorityType.objects.all(), required=False, allow_null=True
    )
    project_start_decision = serializers.PrimaryKeyRelatedField(
        queryset=ProjectStartDecision.objects.all(), required=False, allow_null=True
    )
    address = AddressSerializer()

    class Meta:
        model = ProjectRevision
        fields = (
            "id",
            "project",
            "revision_date",
            "revision_date_eng",
            "process_start_ward",
            "project_name",
            "project_name_eng",
            "address",
            "project_level",
            "project_type",
            "project_nature",
            "work_class",
            "subject_area",
            "strategic_sign",
            "work_proposer_type",
            "priority_type",
            "project_start_decision",
            "first_trimester",
            "second_trimester",
            "third_trimester",
            "fourth_trimester",
            "is_multi_year_plan",
            "first_year",
            "second_year",
            "third_year",
            "forth_year",
            "fifth_year",
            "other",
            "latitude",
            "longitude",
            "appropriated_amount",
            "overhead",
            "contingency",
            "mu_aa_ka",
            "public_charity",
            "maintenance",
            "disaster_mgmt_fund",
            "total_estimate",
            "self_payment",
            "remarks",
            "karmagat",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "revision_date": {"required": False, "allow_null": True},
            "revision_date_eng": {"required": False, "allow_null": True},
            "process_start_ward": {"required": False, "allow_null": True},
            "project_name": {"required": False, "allow_null": True},
            "project_name_eng": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
            "project_level": {"required": False, "allow_null": True},
            "project_type": {"required": False, "allow_null": True},
            "project_nature": {"required": False, "allow_null": True},
            "work_class": {"required": False, "allow_null": True},
            "subject_area": {"required": False, "allow_null": True},
            "strategic_sign": {"required": False, "allow_null": True},
            "work_proposer_type": {"required": False, "allow_null": True},
            "priority_type": {"required": False, "allow_null": True},
            "project_start_decision": {"required": False, "allow_null": True},
            "first_trimester": {"required": False, "allow_null": True},
            "second_trimester": {"required": False, "allow_null": True},
            "third_trimester": {"required": False, "allow_null": True},
            "fourth_trimester": {"required": False, "allow_null": True},
            "is_multi_year_plan": {"required": False, "allow_null": True},
            "first_year": {"required": False, "allow_null": True},
            "second_year": {"required": False, "allow_null": True},
            "third_year": {"required": False, "allow_null": True},
            "forth_year": {"required": False, "allow_null": True},
            "fifth_year": {"required": False, "allow_null": True},
            "other": {"required": False, "allow_null": True},
            "latitude": {"required": False, "allow_null": True},
            "longitude": {"required": False, "allow_null": True},
            "appropriated_amount": {"required": False, "allow_null": True},
            "overhead": {"required": False, "allow_null": True},
            "contingency": {"required": False, "allow_null": True},
            "mu_aa_ka": {"required": False, "allow_null": True},
            "public_charity": {"required": False, "allow_null": True},
            "maintenance": {"required": False, "allow_null": True},
            "disaster_mgmt_fund": {"required": False, "allow_null": True},
            "total_estimate": {"required": False, "allow_null": True},
            "self_payment": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "karmagat": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        read_only_fields = ("id",)

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)
        validated_data["address"] = address
        project_revision = ProjectRevision.objects.create(**validated_data)
        return project_revision

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address")
        if address_data:
            address_serializer = AddressSerializer(instance.address, data=address_data)
            if address_data["municipality"]:
                municipality = address_data.pop("municipality").id
                address_data["municipality"] = municipality
            if address_serializer.is_valid():
                address = address_serializer.save()
                validated_data["address"] = address
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        project_level = instance.project_level
        project_type = instance.project_type
        project_nature = instance.project_nature
        work_class = instance.work_class
        subject_area = instance.subject_area
        strategic_sign = instance.strategic_sign
        priority_type = instance.priority_type
        project_start_decision = instance.project_start_decision
        representation["project"] = self.get_common_data(project) if project else None
        representation["project_level"] = (
            self.get_common_data(project_level) if project_level else None
        )
        representation["project_type"] = (
            self.get_common_data(project_type) if project_type else None
        )
        representation["project_nature"] = (
            self.get_common_data(project_nature) if project_nature else None
        )
        representation["work_class"] = (
            self.get_common_data(work_class) if work_class else None
        )
        representation["subject_area"] = (
            self.get_common_data(subject_area) if subject_area else None
        )
        representation["strategic_sign"] = (
            self.get_common_data(strategic_sign) if strategic_sign else None
        )
        representation["priority_type"] = (
            self.get_common_data(priority_type) if priority_type else None
        )
        representation["project_start_decision"] = (
            self.get_common_data(project_start_decision)
            if project_start_decision
            else None
        )
        return representation


class UserCommitteeDocumentsSerializer(PlanExecutionBaseSerializer):
    class Meta:
        model = UserCommitteeDocuments
        fields = ("id", "document_file", "document_name", "document_size")
        extra_kwargs = {
            "document_name": {"required": False, "allow_null": True},
            "document_size": {"required": False, "allow_null": True},
        }


class UserCommitteeProjectWorkCompleteSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    bank = serializers.PrimaryKeyRelatedField(queryset=BFI.objects.all())
    submitted_by = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    submitted_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all()
    )
    approved_by = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    approved_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all()
    )
    # project_document = UserCommitteeDocumentsSerializer()
    # project_document = serializers.FileField(allow_empty_file=True)
    document_title = serializers.CharField(
        max_length=100, required=False, allow_null=True
    )

    class Meta:
        model = UserCommitteeProjectWorkComplete
        fields = (
            "id",
            "project",
            "ch_no",
            "pa_no",
            "project_complete_date",
            "project_complete_date_eng",
            "bank",
            "account_no",
            "submitted_by",
            "submitted_by_position",
            "approved_by",
            "approved_by_position",
            "bodarth",
            "print_custom_report",
            # "project_document",
            "document_title",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "ch_no": {"required": False, "allow_null": True},
            "pa_no": {"required": False, "allow_null": True},
            "project_complete_date": {"required": False, "allow_null": True},
            "project_complete_date_eng": {"required": False, "allow_null": True},
            "bank": {"required": False, "allow_null": True},
            "account_no": {"required": False, "allow_null": True},
            "submitted_by": {"required": False, "allow_null": True},
            "submitted_by_position": {"required": False, "allow_null": True},
            "approved_by": {"required": False, "allow_null": True},
            "approved_by_position": {"required": False, "allow_null": True},
            "bodarth": {"required": False, "allow_null": True},
            "print_custom_report": {"required": False, "allow_null": True},
            # "project_document": {"required": False, "allow_null": True},
            "document_title": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    # def create(self, validated_data):
    #     project_document = validated_data.pop("project_document")
    #     if project_document:
    #         document_title = validated_data.pop("document_title")
    #         if not document_title:
    #             document_title = project_document.name
    #         file_size = project_document.size
    #         file_content_type = project_document.content_type
    #         file_size_mb = file_size / 1048576
    #
    #         print(
    #             file_size,
    #             file_content_type,
    #             document_title,
    #             project_document,
    #             888880000,
    #         )
    #         project_document_object = UserCommitteeDocuments.objects.create(
    #             document_name=document_title,
    #             document_size=round(file_size_mb, 2),
    #             document=project_document,
    #         )
    #         validated_data["project_document"] = project_document_object
    #     else:
    #         validated_data["project_document"] = project_document
    #     project_complete = UserCommitteeProjectWorkComplete.objects.create(
    #         **validated_data
    #     )
    #     return project_complete

    # def update(self, instance, validated_data):
    #     project_document_data = validated_data.pop("project_document")
    #     if project_document_data:
    #         project_document_serializer = UserCommitteeDocumentsSerializer(
    #             instance.project_document, data=project_document_data
    #         )
    #         if project_document_serializer.is_valid():
    #             project_document = project_document_serializer.save()
    #             validated_data["project_document"] = project_document
    #     return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        bank = instance.bank
        submitted_by = instance.submitted_by
        submitted_by_position = instance.submitted_by_position
        approved_by = instance.approved_by
        approved_by_position = instance.approved_by_position
        representation["project"] = self.get_common_data(project) if project else None
        representation["bank"] = self.get_bank_data(bank) if bank else None
        representation["submitted_by"] = (
            self.emp_data(submitted_by) if submitted_by else None
        )
        representation["submitted_by_position"] = (
            self.get_common_data(submitted_by_position)
            if submitted_by_position
            else None
        )
        representation["approved_by"] = (
            self.emp_data(approved_by) if approved_by else None
        )
        representation["approved_by_position"] = (
            self.get_common_data(approved_by_position) if approved_by_position else None
        )
        return representation

    def emp_data(self, data):
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            "full_name_eng": full_name_eng,
        }

    def get_bank_data(self, data):
        return {
            "id": data.id,
            "code": data.code,
            "full_name": data.full_name,
            "full_name_eng": data.full_name_eng,
            "registration_no": data.registration_no,
            "registration_date": data.registration_date,
            "registration_date_eng": data.registration_date_eng,
            "bank_type": data.bank_type.name if data.bank_type else "",
            "cheque_format": data.cheque_format.name if data.cheque_format else "",
        }


class DepositMandateSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    order_by = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    order_by_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all()
    )
    nominated_employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )
    nominated_employee_position = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSector.objects.all()
    )

    class Meta:
        model = DepositMandate
        fields = (
            "id",
            "project",
            "mandate_type",
            "order_by",
            "order_by_position",
            "order_date",
            "order_date_eng",
            "nominated_employee",
            "nominated_employee_position",
            "invoice_date",
            "invoice_date_eng",
            "invoice_no",
            "latter_no",
            "work_complete_date",
            "work_complete_date_eng",
            "report_custom_print",
            "opinion",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "mandate_type": {"required": False, "allow_null": True},
            "order_by": {"required": False, "allow_null": True},
            "order_by_position": {"required": False, "allow_null": True},
            "order_date": {"required": False, "allow_null": True},
            "order_date_eng": {"required": False, "allow_null": True},
            "nominated_employee": {"required": False, "allow_null": True},
            "nominated_employee_position": {"required": False, "allow_null": True},
            "invoice_date": {"required": False, "allow_null": True},
            "invoice_date_eng": {"required": False, "allow_null": True},
            "invoice_no": {"required": False, "allow_null": True},
            "latter_no": {"required": False, "allow_null": True},
            "work_complete_date": {"required": False, "allow_null": True},
            "work_complete_date_eng": {"required": False, "allow_null": True},
            "report_custom_print": {"required": False, "allow_null": True},
            "opinion": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        order_by = instance.order_by
        order_by_position = instance.order_by_position
        nominated_employee = instance.nominated_employee
        nominated_employee_position = instance.nominated_employee_position
        representation["project"] = self.get_common_data(project) if project else None
        representation["order_by"] = self.emp_data(order_by) if order_by else None
        representation["order_by_position"] = (
            self.get_common_data(order_by_position) if order_by_position else None
        )
        representation["nominated_employee"] = (
            self.emp_data(nominated_employee) if nominated_employee else None
        )
        representation["nominated_employee_position"] = (
            self.get_common_data(nominated_employee_position)
            if nominated_employee_position
            else None
        )
        return representation

    def get_project_document(self, obj):
        return {
            "id": obj.id,
            "document": obj.document.url if obj.document else None,
            "document_size": obj.document_size,
            "document_name": obj.document_name,
        }

    def emp_data(self, data):
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            "full_name_eng": full_name_eng,
        }


class NominatedStaffSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    employee_name = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=EmployeeSector.objects.all())

    class Meta:
        model = InstitutionalCollaborationNominatedStaff
        fields = (
            "id",
            "project",
            "code",
            "employee_name",
            "position",
            "remarks",
            "serial_number",
            "employee_name_by",
            "employee_position_by",
            "employee_name_remarks",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "employee_name": {"required": False, "allow_null": True},
            "position": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "serial_number": {"required": False, "allow_null": True},
            "employee_name_by": {"required": False, "allow_null": True},
            "employee_position_by": {"required": False, "allow_null": True},
            "employee_name_remarks": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        employee_name = instance.employee_name
        position = instance.position

        representation["project"] = self.get_common_data(project) if project else None
        representation["employee_name"] = (
            self.emp_data(employee_name) if employee_name else None
        )
        representation["position"] = (
            self.get_common_data(position) if position else None
        )
        return representation

    def emp_data(self, data):
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            "full_name_eng": full_name_eng,
        }


class InstitutionalCollaborationMandateSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    selected_employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )

    class Meta:
        model = InstitutionalCollaborationMandate
        fields = (
            "id",
            "project",
            "selected_employee",
            "opinion_detail",
            "invoice_number",
            "invoice_number_eng",
            "project_complete_date",
            "project_complete_date_eng",
            "mandate_invoice_no",
            "mandate_letter",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "selected_employee": {"required": False, "allow_null": True},
            "opinion_detail": {"required": False, "allow_null": True},
            "invoice_number": {"required": False, "allow_null": True},
            "invoice_number_eng": {"required": False, "allow_null": True},
            "project_complete_date": {"required": False, "allow_null": True},
            "project_complete_date_eng": {"required": False, "allow_null": True},
            "mandate_invoice_no": {"required": False, "allow_null": True},
            "mandate_letter": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        selected_employee = instance.selected_employee
        representation["project"] = self.get_common_data(project) if project else None
        representation["selected_employee"] = (
            self.emp_data(selected_employee) if selected_employee else None
        )
        return representation

    def emp_data(self, data):
        full_name = f"{data.first_name} {data.middle_name} {data.last_name}"
        full_name_eng = (
            f"{data.first_name_eng} {data.middle_name_eng} {data.last_name_eng}"
        )
        return {
            "id": data.id,
            "code": data.code,
            "full_name": full_name,
            "full_name_eng": full_name_eng,
        }


class ProjectReportFinishedAndUpdateSerializer(PlanExecutionBaseSerializer):
    financial_year = serializers.PrimaryKeyRelatedField(
        queryset=FinancialYear.objects.all()
    )
    address = AddressSerializer()
    project_type = serializers.PrimaryKeyRelatedField(
        queryset=ProjectType.objects.all()
    )
    project_nature = serializers.PrimaryKeyRelatedField(
        queryset=ProjectNature.objects.all()
    )
    work_class = serializers.PrimaryKeyRelatedField(queryset=WorkClass.objects.all())
    subject_area = serializers.PrimaryKeyRelatedField(
        queryset=SubjectArea.objects.all()
    )
    strategic_sign = serializers.PrimaryKeyRelatedField(
        queryset=StrategicSign.objects.all()
    )
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())
    project_priority = serializers.PrimaryKeyRelatedField(
        queryset=PriorityType.objects.all()
    )
    project_level = serializers.PrimaryKeyRelatedField(
        queryset=ProjectLevel.objects.all()
    )
    firm_name = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    consumer_committee_name = serializers.PrimaryKeyRelatedField(
        queryset=ConsumerCommittee.objects.all()
    )
    start_pms_process = serializers.PrimaryKeyRelatedField(
        queryset=StartPmsProcess.objects.all(), required=False, allow_null=True
    )
    plan_start_decision = serializers.PrimaryKeyRelatedField(
        queryset=PlanStartDecision.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectReportFinishedAndUpdate
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "financial_year",
            "ward",
            "address",
            "project_type",
            "project_nature",
            "work_class",
            "subject_area",
            "strategic_sign",
            "work_proposer_type",
            "program",
            "project_priority",
            "start_pms_process",
            "plan_start_decision",
            "project_level",
            "firm_name",
            "quantity",
            "expense_investment",
            "consumer_committee_name",
            "bid_calling_date",
            "bid_calling_date_eng",
            "bid_enter_date",
            "bid_enter_date_eng",
            "karyadesh_date",
            "karyadesh_date_eng",
            "bid_enter_number",
            "news_paper",
            "published_date",
            "published_date_eng",
            "anticipated_completion_date",
            "anticipated_completion_date_eng",
            "agreement_date",
            "agreement_date_eng",
            "internal_source",
            "nepal_gov",
            "province_gov",
            "local_level_gov",
            "public_participation",
            "expense_investment_variation",
            "variation_ru",
            "variation_percent",
            "variation_for_approval",
            "ammended_expense",
            "advanced",
            "paid",
            "blocked_amount",
            "payment_remained",
            "finished_date",
            "finished_date_eng",
            "road_length",
            "road_width",
            "channel_length",
            "channel_depth",
            "drinking_water_pipe_length",
            "kalvert_length",
            "kalvert_width",
            "building_length",
            "building_width",
            "area",
            "total_storey",
            "wall_length",
            "wall_height",
            "source_preservation_area",
            "status",
            "karmagat",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "financial_year": {"required": False, "allow_null": True},
            "ward": {"required": False, "allow_null": True},
            "address": {"required": False, "allow_null": True},
            "project_type": {"required": False, "allow_null": True},
            "project_nature": {"required": False, "allow_null": True},
            "work_class": {"required": False, "allow_null": True},
            "subject_area": {"required": False, "allow_null": True},
            "strategic_sign": {"required": False, "allow_null": True},
            "work_proposer_type": {"required": False, "allow_null": True},
            "program": {"required": False, "allow_null": True},
            "project_priority": {"required": False, "allow_null": True},
            "start_pms_process": {"required": False, "allow_null": True},
            "plan_start_decision": {"required": False, "allow_null": True},
            "project_level": {"required": False, "allow_null": True},
            "firm_name": {"required": False, "allow_null": True},
            "quantity": {"required": False, "allow_null": True},
            "expense_investment": {"required": False, "allow_null": True},
            "consumer_committee_name": {"required": False, "allow_null": True},
            "bid_calling_date": {"required": False, "allow_null": True},
            "bid_calling_date_eng": {"required": False, "allow_null": True},
            "bid_enter_date": {"required": False, "allow_null": True},
            "bid_enter_date_eng": {"required": False, "allow_null": True},
            "karyadesh_date": {"required": False, "allow_null": True},
            "karyadesh_date_eng": {"required": False, "allow_null": True},
            "bid_enter_number": {"required": False, "allow_null": True},
            "news_paper": {"required": False, "allow_null": True},
            "published_date": {"required": False, "allow_null": True},
            "published_date_eng": {"required": False, "allow_null": True},
            "anticipated_completion_date": {"required": False, "allow_null": True},
            "anticipated_completion_date_eng": {"required": False, "allow_null": True},
            "agreement_date": {"required": False, "allow_null": True},
            "agreement_date_eng": {"required": False, "allow_null": True},
            "internal_source": {"required": False, "allow_null": True},
            "nepal_gov": {"required": False, "allow_null": True},
            "province_gov": {"required": False, "allow_null": True},
            "local_level_gov": {"required": False, "allow_null": True},
            "public_participation": {"required": False, "allow_null": True},
            "expense_investment_variation": {"required": False, "allow_null": True},
            "variation_ru": {"required": False, "allow_null": True},
            "variation_percent": {"required": False, "allow_null": True},
            "variation_for_approval": {"required": False, "allow_null": True},
            "ammended_expense": {"required": False, "allow_null": True},
            "advanced": {"required": False, "allow_null": True},
            "paid": {"required": False, "allow_null": True},
            "blocked_amount": {"required": False, "allow_null": True},
            "payment_remained": {"required": False, "allow_null": True},
            "finished_date": {"required": False, "allow_null": True},
            "finished_date_eng": {"required": False, "allow_null": True},
            "road_length": {"required": False, "allow_null": True},
            "road_width": {"required": False, "allow_null": True},
            "channel_length": {"required": False, "allow_null": True},
            "channel_depth": {"required": False, "allow_null": True},
            "drinking_water_pipe_length": {"required": False, "allow_null": True},
            "kalvert_length": {"required": False, "allow_null": True},
            "kalvert_width": {"required": False, "allow_null": True},
            "building_length": {"required": False, "allow_null": True},
            "building_width": {"required": False, "allow_null": True},
            "area": {"required": False, "allow_null": True},
            "total_storey": {"required": False, "allow_null": True},
            "wall_length": {"required": False, "allow_null": True},
            "wall_height": {"required": False, "allow_null": True},
            "source_preservation_area": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "karmagat": {"required": False, "allow_null": True},
        }

    def create(self, request_data):
        address = request_data.pop("address")
        address = Address.objects.create(**address)
        request_data["address"] = address
        user_committee = ProjectReportFinishedAndUpdate.objects.create(**request_data)
        return user_committee

    def update(self, instance, request_data):
        address_data = request_data.pop("address")
        if address_data:
            address_serializer = AddressSerializer(instance.address, data=address_data)
            if address_data["municipality"]:
                municipality = address_data.pop("municipality").id
                address_data["municipality"] = municipality
            if address_serializer.is_valid():
                address = address_serializer.save()
                request_data["address"] = address
        return super().update(instance, request_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        financial_year = instance.financial_year
        address = instance.address
        project_type = instance.project_type
        project_nature = instance.project_nature
        work_class = instance.work_class
        subject_area = instance.subject_area
        strategic_sign = instance.strategic_sign
        program = instance.program
        project_priority = instance.project_priority
        project_level = instance.project_level
        firm_name = instance.firm_name
        consumer_committee_name = instance.consumer_committee_name
        start_pms_process = instance.start_pms_process
        plan_start_decision = instance.plan_start_decision

        data["address"] = self.get_address(address) if address else "-"
        data["financial_year"] = (
            self.get_financial_year(financial_year) if financial_year else "-"
        )
        data["project_type"] = (
            self.get_common_data(project_type) if project_type else "-"
        )
        data["project_nature"] = (
            self.get_common_data(project_nature) if project_nature else "-"
        )
        data["work_class"] = self.get_common_data(work_class) if work_class else "-"
        data["subject_area"] = (
            self.get_common_data(subject_area) if subject_area else "-"
        )
        data["strategic_sign"] = (
            self.get_common_data(strategic_sign) if strategic_sign else "-"
        )
        data["program"] = self.get_common_data(program) if program else "-"
        data["project_priority"] = (
            self.get_common_data(project_priority) if project_priority else "-"
        )
        data["project_level"] = (
            self.get_common_data(project_level) if project_level else "-"
        )
        data["firm_name"] = self.get_common_data(firm_name) if firm_name else "-"
        data["consumer_committee_name"] = (
            self.get_common_data(consumer_committee_name)
            if consumer_committee_name
            else "-"
        )
        data["start_pms_process"] = (
            self.get_common_data(start_pms_process) if start_pms_process else "-"
        )
        data["plan_start_decision"] = (
            self.get_common_data(plan_start_decision) if plan_start_decision else "-"
        )
        return data

    @staticmethod
    def get_address(data):
        return {
            "local_level": data.local_level,
            "local_level_eng": data.local_level_eng,
            "ward": data.ward,
            "ward_eng": data.ward_eng,
        }

    @staticmethod
    def get_financial_year(data):
        return {
            "id": data.id,
            "start_year": data.start_year,
            "end_year": data.end_year,
            "fy": data.fy,
        }


class OfficialProcessRemarkFileSerializer(PlanExecutionBaseSerializer):
    class Meta:
        model = OfficialProcessRemarkFile
        fields = (
            "file",
            "filename",
            "status",
            "official_process",
        )
        extra_kwargs = {
            "file": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class OfficialProcessLogSerializer(PlanExecutionBaseSerializer):
    official_process_files = OfficialProcessRemarkFileSerializer(
        many=True, required=False, allow_null=True
    )

    class Meta:
        model = OfficialProcess
        fields = (
            "id",
            "request_by",
            "send_to",
            "send_for",
            "remarks",
            "file",
            "project",
            "status",
            "feedback_remarks",
            "feedback_file",
            "official_process_files",
            "status_of_model",
        )
        extra_kwargs = {
            "request_by": {"required": False, "allow_null": True},
            "send_to": {"required": False, "allow_null": True},
            "send_for": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "file": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "feedback_remarks": {"required": False, "allow_null": True},
            "feedback_file": {"required": False, "allow_null": True},
            "status_of_model": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request_by = instance.request_by
        send_to = instance.send_to
        send_for = instance.send_for
        file = instance.file
        status = instance.status
        project = instance.project
        feedback_file = instance.feedback_file

        data["request_by"] = self.get_user(request_by) if request_by else None
        data["send_to"] = self.get_user(send_to) if send_to else None
        data["send_for"] = self.get_request_type(send_for) if send_for else None
        data["status"] = self.get_status(status) if status else None
        data["file"] = self.get_file(file) if file else None
        data["feedback_file"] = self.get_file(feedback_file) if feedback_file else None
        data["date"] = ad_to_bs(instance.created_date.date())
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


class OfficialProcessRequestSerializer(PlanExecutionBaseSerializer):
    """create preparation"""

    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    remarks = serializers.CharField(required=False, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True)
    official_process_files = OfficialProcessRemarkFileSerializer(
        many=True, required=False, allow_null=True, read_only=True
    )
    remark_files = serializers.ListField(
        child=serializers.FileField(required=False, allow_null=True)
    )

    class Meta:
        model = OfficialProcess
        fields = (
            "request_by",
            "send_to",
            "send_for",
            "remarks",
            "file",
            "parent_process",
            "official_process_files",
            "project",
            "status",
            "remark_files",
        )
        extra_kwargs = {
            "request_by": {"required": False, "allow_null": True},
            "send_to": {"required": False, "allow_null": True},
            "send_for": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "file": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def save(self, **kwargs):
        save_return = super().save(**kwargs)

        if self.validated_data.get("remark_files"):
            for file in self.validated_data.get("remark_files"):
                OfficialProcessRemarkFile.objects.create(
                    file=file, official_process=self.instance
                )

        return save_return


class ApprovalVerificationSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    feedback_remarks = serializers.CharField(required=False, allow_null=True)
    feedback_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = OfficialProcess
        fields = (
            "id",
            "project",
            "status",
            "feedback_remarks",
            "feedback_file",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "feedback_remarks": {"required": False, "allow_null": True},
            "feedback_file": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        read_only_fields = ("id",)


class ConstantSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class CommentAndOrderSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = CommentAndOrder
        fields = ("id", "project", "cha_no", "status")
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "cha_no": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class ProjectExecutionDocumentSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    name = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = ProjectExecutionDocument
        fields = ("id", "document", "project", "doc_type", "name", "doc_size")

    def create(self, validated_data):
        document = validated_data.get("document")
        if document:
            content_type = document.content_type
            file_name = document.name
            file_size = document.size
            validated_data["doc_type"] = content_type
            validated_data["name"] = ""
            validated_data["doc_size"] = f"{round(int(file_size) / 1024, 2)}KB"
        return super().create(validated_data)


class ProjectCommentRemarkFileSerializer(PlanExecutionBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    filename = serializers.CharField(required=False, allow_null=True)
    status = serializers.BooleanField(default=True)

    class Meta:
        model = ProjectCommentRemarkFile
        fields = ("id", "file", "filename", "status")
        extra_kwargs = {
            "file": {"required": False, "allow_null": True},
            "filename": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class IndividualProjectCommentSerializer(PlanExecutionBaseSerializer):
    individual_comment_files = ProjectCommentRemarkFileSerializer(
        many=True, required=False, allow_null=True
    )

    class Meta:
        model = IndividualProjectComment
        fields = ("id", "comment", "comment_date_time", "individual_comment_files")
        extra_kwargs = {
            "comment": {"required": False, "allow_null": True},
            "comment_date_time": {"required": False, "allow_null": True},
            "individual_comment_files": {"required": False, "allow_null": True},
        }


class ProjectCommentSerializer(PlanExecutionBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    request_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    is_draft = serializers.BooleanField(default=False)
    is_signed = serializers.BooleanField(default=False)
    start_pms_process = serializers.PrimaryKeyRelatedField(
        queryset=StartPmsProcess.objects.all(), required=False, allow_null=True
    )
    process_name = serializers.ChoiceField(
        choices=ProcessNameChoices.choices, required=False, allow_null=True
    )
    send_for = serializers.ChoiceField(
        choices=CommentSentForChoices.choices, required=False, allow_null=True
    )
    status = serializers.ChoiceField(
        choices=CommentStatusChoices.choices, default=CommentStatusChoices.PENDING
    )
    # Deprecating Soon
    send_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    remarks = serializers.CharField(required=False, allow_null=True)
    remark_files = serializers.ListField(
        child=serializers.FileField(required=False, allow_null=True),
        write_only=True,
        required=False,
        allow_null=True,
    )
    individual_comments = IndividualProjectCommentSerializer(
        many=True, required=False, allow_null=True
    )
    users_allowed_to_comment = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()),
        required=False,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = ProjectComment
        fields = (
            "id",
            "project",
            "request_by",
            "is_draft",
            "is_signed",
            "start_pms_process",
            "process_name",
            "send_for",
            "status",
            "individual_comments",
            "users_allowed_to_comment",
            "send_to",
            "remarks",
            "remark_files",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "request_by": {"required": False, "allow_null": True},
            "is_draft": {"required": False, "allow_null": True},
            "is_signed": {"required": False, "allow_null": True},
            "start_pms_process": {"required": False, "allow_null": True},
            "process_name": {"required": False, "allow_null": True},
            "send_for": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "individual_comments": {"required": False, "allow_null": True},
            "users_allowed_to_comment": {"required": False, "allow_null": True},
            "send_to": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "remark_files": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        remark_files = validated_data.pop("remark_files", [])
        remark_file_objects = []
        if remark_files:
            for remark_file in remark_files:
                remark_file_objects.append(
                    ProjectCommentRemarkFile.objects.create(file=remark_file)
                )
        project_comment = ProjectComment.objects.create(**validated_data)
        if remark_file_objects:
            project_comment.remark_files.set(remark_file_objects)
        return project_comment

    def validate(self, attrs):
        # if attrs.get("request_by") != self.context["request"].user:
        #     raise serializers.ValidationError(
        #         {"request_by": "Request by must be current user"}
        #     )
        if (
            attrs.get("request_by").assigned_municipality
            != attrs.get("project").municipality
            or attrs.get("send_to").assigned_municipality
            != attrs.get("project").municipality
        ):
            raise serializers.ValidationError(
                {"project": "Comment should be for the municipality's project"}
            )
        return super().validate(attrs)

    @staticmethod
    def get_user(data):
        return {
            "id": data.id,
            "username": data.username,
            "full_name": data.full_name or "",
            "email": data.email,
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["request_by"] = self.get_user(instance.request_by)
        representation["send_to"] = self.get_user(instance.send_to)
        representation["process_name"] = instance.get_process_name_display()
        representation["send_for"] = instance.get_send_for_display()
        representation["status"] = instance.get_status_display()
        if instance.users_allowed_to_comment.exists():
            representation["users_allowed_to_comment"] = [
                self.get_user(user) for user in instance.users_allowed_to_comment.all()
            ]
        else:
            representation["users_allowed_to_comment"] = [
                self.get_user(user) for user in instance.users_allowed_to_comment.all()
            ]
        if instance.remark_files.exists():
            representation["remark_files"] = ProjectCommentRemarkFileSerializer(
                instance.remark_files.all(),
                many=True,
                context={"request": self.context.get("request")},
            ).data
        if instance.project:
            representation["project"] = ProjectExecutionSerializer(
                instance.project
            ).data
        if instance.start_pms_process:
            representation["start_pms_process"] = StartPmsProcessSerializer(
                instance.start_pms_process
            ).data
        return representation


# Quotation Serializers


class FirmQuotedCostEstimateSerializer(BaseSerializer):
    cost_estimate_data_id = serializers.PrimaryKeyRelatedField(
        queryset=CostEstimateData.objects.all(), source="cost_estimate_data"
    )
    description = serializers.CharField(
        source="cost_estimate_data.description", read_only=True
    )
    unit = serializers.CharField(source="cost_estimate_data.unit", read_only=True)
    quantity = serializers.CharField(
        source="cost_estimate_data.quantity", read_only=True
    )

    class Meta:
        model = FirmQuotedCostEstimate
        fields = (
            "id",
            "cost_estimate_data_id",
            "description",
            "unit",
            "quantity",
            "rate",
            "amount",
            "is_vat_added",
        )


class CostEstimateDataSerializer(BaseSerializer):
    quot_specification = serializers.PrimaryKeyRelatedField(
        queryset=QuotationSpecification.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CostEstimateData
        fields = (
            "id",
            "quot_specification",
            "description",
            "unit",
            "quantity",
            "rate",
            "amount",
            "remarks",
            "status",
        )


class QuotationFirmDetailsSerializer(BaseSerializer):
    quot_specification = serializers.PrimaryKeyRelatedField(
        queryset=QuotationSpecification.objects.all(),
        required=False,
        allow_null=True,
    )
    municipality = serializers.PrimaryKeyRelatedField(
        queryset=Municipality.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = QuotationFirmDetails
        fields = (
            "id",
            "firm_name",
            "registration_number",
            "pan_no",
            "municipality",
            "ward",
            "tole",
            "quot_specification",
            "status",
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["municipality"] = SimpleMunicipalitySerializer(instance.municipality).data
        return rep


class QuotationSpecificationSerializer(WriteableNestedModelBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    cost_estimate_data = CostEstimateDataSerializer(
        many=True, required=False, allow_null=True
    )
    firm_details = QuotationFirmDetailsSerializer(
        source="specification_firm_details", many=True, read_only=True
    )

    class Meta:
        model = QuotationSpecification
        fields = (
            "id",
            "project",
            "boq_type",
            "cha_no",
            "letter_no",
            "cost_estimate_data",
            "firm_details",
            "date",
            "date_eng",
            "status",
        )


class QuotationInvitationForProposalSerializer(BaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    firm_name = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), source="invited_firm.firm_name"
    )
    registration_number = serializers.CharField(
        source="invited_firm.registration_number"
    )
    pan_no = serializers.CharField(source="invited_firm.pan_no")

    class Meta:
        model = QuotationInvitationForProposal
        fields = (
            "id",
            "project",
            "letter_no",
            "cha_no",
            "firm_name",
            "registration_number",
            "pan_no",
        )

    def create(self, validated_data):
        invited_firm_data = validated_data.pop("invited_firm")
        quotation_invitation_for_proposal = (
            QuotationInvitationForProposal.objects.create(**validated_data)
        )
        invited_firm = QuotationFirmDetails.objects.create(
            quot_specification=quotation_invitation_for_proposal.quot_specification,
            **invited_firm_data,
        )
        quotation_invitation_for_proposal.invited_firm = invited_firm
        quotation_invitation_for_proposal.save()
        return quotation_invitation_for_proposal

    def update(self, instance, validated_data):
        invited_firm_data = validated_data.pop("invited_firm")
        invited_firm_id = instance.invited_firm.id if instance.invited_firm else -1
        invited_firm, invited_firm_created = None, False
        if any(invited_firm_data.values()):
            (
                invited_firm,
                invited_firm_created,
            ) = QuotationFirmDetails.objects.update_or_create(
                id=invited_firm_id, defaults=invited_firm_data
            )
        updated_instance = super().update(instance, validated_data)
        if invited_firm_created and invited_firm:
            updated_instance.invited_firm = invited_firm
            updated_instance.save()

        return updated_instance


class SubmissionApprovalFirmDetailsSerializer(WriteableNestedModelBaseSerializer):
    cost_estimate_data = FirmQuotedCostEstimateSerializer(
        source="quoted_cost_estimates", many=True, required=False, allow_null=True
    )
    firm_name = serializers.StringRelatedField(read_only=True)
    municipality = serializers.PrimaryKeyRelatedField(
        queryset=Municipality.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = QuotationFirmDetails
        fields = (
            "id",
            "firm_name",
            "registration_number",
            "pan_no",
            "municipality",
            "ward",
            "tole",
            "cost_estimate_data",
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["municipality"] = SimpleMunicipalitySerializer(instance.municipality).data
        return rep


class SubmissionApprovalFirmDetailsUpdateSerializer(WriteableNestedModelBaseSerializer):
    cost_estimate_data = FirmQuotedCostEstimateSerializer(
        source="quoted_cost_estimates", many=True, required=False, allow_null=True
    )

    class Meta:
        model = QuotationFirmDetails
        fields = (
            "id",
            "cost_estimate_data",
        )


class QuotationSubmissionApprovalSerializer(WriteableNestedModelBaseSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all()
    )
    firm_details = SubmissionApprovalFirmDetailsSerializer(
        source="submission_approval_firm_details",
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = QuotationSubmissionApproval
        fields = (
            "id",
            "project",
            "cha_no",
            "letter_no",
            "date",
            "date_eng",
            "firm_details",
            "status",
        )
