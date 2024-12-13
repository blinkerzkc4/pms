from datetime import datetime

from django_filters import rest_framework as filters

from base_model.models import DocumentType
from budget_process.models import (
    BudgetAmmendment,
    BudgetExpenseManagement,
    BudgetManagement,
    BudgetTransfer,
    EstimateFinancialArrangements,
    ExpenseBudgetRangeDetermine,
    IncomeBudgetRangeDetermine,
)
from employee.models import (
    Department,
    Employee,
    EmployeeSector,
    EmployeeType,
    Position,
    PositionLevel,
    PublicRepresentativeDetail,
    PublicRepresentativePosition,
)
from formulate_plan.models import ProjectDocument, ProjectWorkType, WorkProject
from plan_execution.models import ProjectExecution
from project.models import Project
from project_report.models import CustomReportTemplate, ReportType

from .models import *


class ExpanseTypeFilter(filters.FilterSet):
    class Meta:
        model = ExpanseType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ProjectTypeFilter(filters.FilterSet):
    class Meta:
        model = ProjectType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "parent": ["exact"],
            "status": ["exact"],
        }


class PurposePlanFilter(filters.FilterSet):
    class Meta:
        model = PurposePlan
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ProjectProcessFilter(filters.FilterSet):
    class Meta:
        model = ProjectProcess
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ProjectNatureFilter(filters.FilterSet):
    class Meta:
        model = ProjectNature
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ProjectLevelFilter(filters.FilterSet):
    class Meta:
        model = ProjectLevel
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ProjectProposedTypeFilter(filters.FilterSet):
    class Meta:
        model = ProjectProposedType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ProjectActivityFilter(filters.FilterSet):
    class Meta:
        model = ProjectActivity
        fields = {
            "name": ["icontains"],
            "code": ["exact"],
            "status": ["exact"],
        }


class PurchaseTypeFilter(filters.FilterSet):
    class Meta:
        model = PurchaseType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class PriorityTypeFilter(filters.FilterSet):
    class Meta:
        model = PriorityType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class SelectionFeasibilityFilter(filters.FilterSet):
    class Meta:
        model = SelectionFeasibility
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class StrategicSignFilter(filters.FilterSet):
    class Meta:
        model = StrategicSign
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ProgramFilter(filters.FilterSet):
    class Meta:
        model = Program
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "name_eng": ["icontains"],
        }


class TargetGroupFilter(filters.FilterSet):
    class Meta:
        model = TargetGroup
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "target_group_category": ["exact"],
        }


class UnitFilter(filters.FilterSet):
    class Meta:
        model = Unit
        fields = {
            "name_unicode": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ProjectStatusFilter(filters.FilterSet):
    class Meta:
        model = ProjectStatus
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ContractorTypeFilter(filters.FilterSet):
    class Meta:
        model = ContractorType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ExecutiveAgencyFilter(filters.FilterSet):
    class Meta:
        model = ExecutiveAgency
        fields = {
            "name": ["icontains"],
            "code": ["exact"],
            "status": ["exact"],
        }


class RoadStatusFilter(filters.FilterSet):
    class Meta:
        model = RoadStatus
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class RoadTypeFilter(filters.FilterSet):
    class Meta:
        model = RoadType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class DrainageTypeFilter(filters.FilterSet):
    class Meta:
        model = DrainageType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class RoadFilter(filters.FilterSet):
    class Meta:
        model = Road
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "connected_wards": ["exact"],
            "average_width": ["exact"],
            "drainage_type": ["exact"],
            "drainage_length": ["exact"],
            "drainage_width": ["exact"],
            "drainage_exit_status": ["exact"],
            "status": ["exact"],
        }


class StandingListTypeFilter(filters.FilterSet):
    class Meta:
        model = StandingListType
        fields = {
            "name": ["icontains"],
            "name_eng": ["icontains"],
            "code": ["exact"],
        }


class StandingListFilter(filters.FilterSet):
    class Meta:
        model = StandingList
        fields = {
            "date": ["exact"],
            "date_eng": ["exact"],
            "organization": ["exact"],
            "financial_year": ["exact"],
            "standing_list_type": ["exact"],
        }


class OfficeFilter(filters.FilterSet):
    class Meta:
        model = Office
        fields = {
            "code": ["exact"],
            "organization_type": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class SourceBearerEntityTypeFilter(filters.FilterSet):
    class Meta:
        model = SourceBearerEntityType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class SourceBearerEntityFilter(filters.FilterSet):
    class Meta:
        model = SourceBearerEntity
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class DocumentTypeFilter(filters.FilterSet):
    class Meta:
        model = DocumentType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "name_eng": ["icontains"],
            "status": ["exact"],
        }


class BudgetSourceFilter(filters.FilterSet):
    class Meta:
        model = BudgetSource
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "name_eng": ["icontains"],
            "phone_number": ["exact"],
            "email": ["exact"],
            "address": ["icontains"],
        }


class AtmFilter(filters.FilterSet):
    class Meta:
        model = BudgetSource
        fields = {
            "name": ["icontains"],
            "name_eng": ["icontains"],
            "code": ["exact"],
            "phone_number": ["exact"],
            "email": ["exact"],
            "address": ["icontains"],
        }


class NewsPaperFilter(filters.FilterSet):
    class Meta:
        model = NewsPaper
        fields = {
            "name": ["icontains"],
            "printing_house": ["icontains"],
        }


class OrganizationFilter(filters.FilterSet):
    class Meta:
        model = Organization
        fields = {
            "code": ["exact"],
            "organization_type": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class BankAccountFilter(filters.FilterSet):
    class Meta:
        model = BankAccount
        fields = {
            "account_no": ["exact"],
            "name": ["icontains"],
            "currency": ["exact"],
            "sub_module": ["exact"],
            "bank_name": ["exact"],
            "status": ["exact"],
        }


class FinancialYearFilter(filters.FilterSet):
    # code = filters.CharFilter(field_name="code", lookup_expr="exact")
    start_year = filters.NumberFilter(field_name="start_year", lookup_expr="gte")
    end_year = filters.NumberFilter(field_name="end_year", lookup_expr="lte")
    status = filters.BooleanFilter(field_name="status", lookup_expr="exact")

    class Meta:
        model = FinancialYear
        fields = ["start_year", "end_year", "status"]


class CurrencyFilter(filters.FilterSet):
    class Meta:
        model = Currency
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class SubjectAreaFilter(filters.FilterSet):
    class Meta:
        model = SubjectArea
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
        }


class SubModuleFilter(filters.FilterSet):
    class Meta:
        model = SubModule
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            # 'module': ['exact'],
            "status": ["exact"],
        }


class ProjectStartDecisionFilter(filters.FilterSet):
    class Meta:
        model = ProjectStartDecision
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ConstructionMaterialDescriptionFilter(filters.FilterSet):
    class Meta:
        model = ConstructionMaterialDescription
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class BudgetSubTitleFilter(filters.FilterSet):
    class Meta:
        model = BudgetSubTitle
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class SourceReceiptFilter(filters.FilterSet):
    class Meta:
        model = SourceReceipt
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class CollectPaymentFilter(filters.FilterSet):
    class Meta:
        model = CollectPayment
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class PaymentMethodFilter(filters.FilterSet):
    class Meta:
        model = PaymentMethod
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class SubLedgerFilter(filters.FilterSet):
    class Meta:
        model = SubLedger
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class AccountTitleManagementFilter(filters.FilterSet):
    class Meta:
        model = AccountTitleManagement
        fields = {
            "code": ["exact"],
            "name_eng": ["icontains"],
            "module": ["exact"],
            "financial_year": ["exact"],
            "status": ["exact"],
            "parent": ["exact"],
        }


class BankTypeFilter(filters.FilterSet):
    class Meta:
        model = BankType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class BFIFilter(filters.FilterSet):
    class Meta:
        model = BFI
        fields = {
            "code": ["exact"],
            "bank_type": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class OrganizationTypeFilter(filters.FilterSet):
    class Meta:
        model = OrganizationType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class MonitoringCommitteeDocumentFilter(filters.FilterSet):
    monitoring_committee_id = filters.NumberFilter(
        field_name="monitoring_committee__id", lookup_expr="exact"
    )

    class Meta:
        model = MonitoringCommitteeDocument
        fields = {
            "status": ["exact"],
        }


class MonitoringCommitteeMemberFilter(filters.FilterSet):
    monitoring_committee_id = filters.NumberFilter(
        field_name="monitoring_committee__id", lookup_expr="exact"
    )

    class Meta:
        model = MonitoringCommitteeMember
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class MonitoringCommitteeFilter(filters.FilterSet):
    class Meta:
        model = MonitoringCommittee
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ConsumerCommitteeDocumentFilter(filters.FilterSet):
    consumer_committee_id = filters.NumberFilter(
        field_name="consumer_committee__id", lookup_expr="exact"
    )

    class Meta:
        model = ConsumerCommitteeDocument
        fields = {
            "status": ["exact"],
        }


class ConsumerCommitteeMemberFilter(filters.FilterSet):
    consumer_committee_id = filters.NumberFilter(
        field_name="consumer_committee__id", lookup_expr="exact"
    )

    class Meta:
        model = ConsumerCommitteeMember
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ConsumerCommitteeFilter(filters.FilterSet):
    class Meta:
        model = ConsumerCommittee
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class ProjectWorkTypeFilter(filters.FilterSet):
    class Meta:
        model = ProjectWorkType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


# need to be add more fields
class WorkProjectFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    proposed_date_eng_from = filters.CharFilter(
        method="filter_by_proposed_date_eng_from"
    )
    proposed_date_eng_to = filters.CharFilter(method="filter_by_proposed_date_eng_to")
    local_level = filters.CharFilter(
        field_name="adddress__local_level", lookup_expr="icontains"
    )

    class Meta:
        model = WorkProject
        fields = [
            "code",
            "name",
            "work_class",
            "work_type",
            "proposed_financial_year",
            "proposed_type",
            "user_committee",
            "ward",
            "local_level",
        ]
        # fields = {
        #     'code': ['exact'],
        #     'name': ['icontains'],
        #     'work_class': ['exact'],
        #     'work_type': ['exact'],
        #     'proposed_type': ['exact'],
        #     'user_committee': ['exact'],
        #     'ward': ['exact'],

        # }

    def filter_by_proposed_date_eng_from(self, queryset, name, value):
        try:
            from_date_value = datetime.strptime(value, "%Y/%m/%d").date()
            return queryset.filter(your_date_field__gte=from_date_value)
        except ValueError:
            return queryset

    def filter_by_proposed_date_eng_to(self, queryset, name, value):
        try:
            to_date_value = datetime.strptime(value, "%Y/%m/%d").date()
            return queryset.filter(your_date_field__lte=to_date_value)
        except ValueError:
            return queryset


class ProjectDocumentFilter(filters.FilterSet):
    code = filters.CharFilter(field_name="project__code", lookup_expr="exact")
    project = filters.CharFilter(field_name="project__id", lookup_expr="exact")
    report_codes = filters.ModelMultipleChoiceFilter(
        field_name="report_type__code",
        to_field_name="code",
        queryset=ReportType.objects.all(),
    )
    name = filters.CharFilter(field_name="project__name", lookup_expr="icontains")

    class Meta:
        model = ProjectDocument
        fields = ["code", "name", "status", "project"]


class ExpenseBudgetRangeDetermineFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="name", lookup_expr="exact")
    financial_year = filters.CharFilter(
        field_name="financial_year", lookup_expr="exact"
    )
    is_approved = filters.BooleanFilter(
        field_name="approve_process__is_approved", lookup_expr="exact"
    )

    class Meta:
        model = ExpenseBudgetRangeDetermine
        fields = ["status", "financial_year", "is_approved"]


class IncomeBudgetRangeDetermineFilter(filters.FilterSet):
    class Meta:
        model = IncomeBudgetRangeDetermine
        fields = {
            "financial_year": ["exact"],
            "status": ["exact"],
        }


class BudgetExpenseManagementFilter(filters.FilterSet):
    parent = filters.CharFilter(field_name="expense_title__id", lookup_expr="exact")

    class Meta:
        model = BudgetExpenseManagement
        fields = ["financial_year", "status", "parent"]


class EstimateFinancialArrangementsFilter(filters.FilterSet):
    class Meta:
        model = EstimateFinancialArrangements
        fields = {
            "financial_year": ["exact"],
            "status": ["exact"],
        }


class EmployeeFilter(filters.FilterSet):
    code = filters.CharFilter(field_name="code", lookup_expr="exact")
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    middle_name = filters.CharFilter(field_name="middle_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    department = filters.CharFilter(
        field_name="current_working_details__department", lookup_expr="exact"
    )
    position = filters.CharFilter(
        field_name="current_working_details__position", lookup_expr="exact"
    )
    service_group = filters.CharFilter(
        field_name="current_working_details__service_group", lookup_expr="exact"
    )
    employee_type = filters.CharFilter(
        field_name="current_working_details__employee_type", lookup_expr="exact"
    )
    work_area = filters.CharFilter(
        field_name="current_working_details__work_area", lookup_expr="exact"
    )
    start_date = filters.CharFilter(method="filter_by_start_date")
    end_date = filters.CharFilter(method="filter_by_end_date")

    class Meta:
        model = Employee
        fields = [
            "subject_area",
            "code",
            "gender",
            "first_name",
            "middle_name",
            "last_name",
            "department",
            "position",
            "service_group",
            "employee_type",
            "work_area",
            "status",
        ]

    def filter_by_start_date(self, queryset, name, value):
        try:
            start_date_value = datetime.strptime(value, "%Y/%m/%d").date()
            return queryset.filter(enrollment_detail__start_date__gte=start_date_value)
        except ValueError:
            return queryset

    def filter_by_end_date(self, queryset, name, value):
        try:
            end_date_value = datetime.strptime(value, "%Y/%m/%d").date()
            return queryset.filter(enrollment_detail__end_date__lte=end_date_value)
        except ValueError:
            return queryset


class DepartmentFilter(filters.FilterSet):
    class Meta:
        model = Department
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "name_eng": ["icontains"],
        }


class EmployeeTypeFilter(filters.FilterSet):
    class Meta:
        model = EmployeeType
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "name_eng": ["icontains"],
        }


class EmployeeSectorFilter(filters.FilterSet):
    class Meta:
        model = EmployeeSector
        fields = {
            "name": ["icontains"],
            # "name_eng": ["icontains"],
        }


class PositionLevelFilter(filters.FilterSet):
    class Meta:
        model = PositionLevel
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "name_eng": ["icontains"],
        }


class PositionFilter(filters.FilterSet):
    class Meta:
        model = Position
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "name_eng": ["icontains"],
        }


class PublicRepresentativePositionFilter(filters.FilterSet):
    class Meta:
        model = PublicRepresentativePosition
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }


class PublicRepresentativeDetailFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="first_name", lookup_expr="exact")
    representative_position = filters.CharFilter(
        field_name="representative_position", lookup_expr="exact"
    )
    position_level = filters.CharFilter(
        field_name="position_level", lookup_expr="exact"
    )
    position_start_date_eng = filters.CharFilter(
        method="filter_by_position_start_date_eng"
    )
    position_end_date_eng = filters.CharFilter(method="filter_by_position_end_date_eng")
    status = filters.CharFilter(field_name="status", lookup_expr="exact")

    class Meta:
        model = PublicRepresentativeDetail
        fields = [
            "name",
            "representative_position",
            "position_level",
            "status",
        ]

    def filter_by_position_start_date_eng(self, queryset, name, value):
        try:
            start_date_value = datetime.strptime(value, "%Y/%m/%d").date()
            return queryset.filter(position_start_date_eng__gte=start_date_value)
        except ValueError:
            return queryset

    def filter_by_position_end_date_eng(self, queryset, name, value):
        try:
            end_date_value = datetime.strptime(value, "%Y/%m/%d").date()
            return queryset.filter(position_end_date_eng__lte=end_date_value)
        except ValueError:
            return queryset


class BudgetTransferFilter(filters.FilterSet):
    allocation_id = filters.NumberFilter(field_name="id", lookup_expr="exact")
    status = filters.BooleanFilter(
        field_name="status",
    )

    class Meta:
        model = BudgetTransfer
        fields = ["allocation_id", "status"]


class BudgetAmmendmentFilter(filters.FilterSet):
    code = filters.CharFilter(
        field_name="account_title__optional_code", lookup_expr="exact"
    )
    name = filters.CharFilter(
        field_name="account_title__display_name", lookup_expr="exact"
    )
    status = filters.BooleanFilter(field_name="status", lookup_expr="exact")

    class Meta:
        model = BudgetAmmendment
        fields = ["code", "name", "status"]


class BudgetManagementFilter(filters.FilterSet):
    code = filters.CharFilter(field_name="code", lookup_expr="exact")

    class Meta:
        model = BudgetManagement
        fields = ["code"]


class CustomReportTemplateFilter(filters.FilterSet):
    report_name = filters.NumberFilter(
        field_name="template_type_id__id", lookup_expr="exact"
    )
    pms_process_id = filters.NumberFilter(
        field_name="start_pms_process__id", lookup_expr="exact"
    )

    class Meta:
        model = CustomReportTemplate
        fields = [
            "pms_process_id",
            "name",
            "name_eng",
            "report_name",
            "is_ward_template",
            "is_new_template",
        ]
