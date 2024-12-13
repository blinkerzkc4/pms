from django_filters import rest_framework as filters

from plan_execution.models import (
    BudgetAllocationDetail,
    OpeningContractAccount,
    ProjectExecution,
    ProjectInstallment,
)
from project.models import Ward


class ProjectInstallmentFilter(filters.FilterSet):
    pms_process_id = filters.CharFilter(
        field_name="start_pms_process__id", lookup_expr="exact"
    )

    class Meta:
        model = ProjectInstallment
        fields = ("code",)


class BudgetAllocationDetailFilter(filters.FilterSet):
    project_id = filters.CharFilter(field_name="project__id", lookup_expr="exact")

    class Meta:
        model = BudgetAllocationDetail
        fields = ("project__id",)


class ProjectExecutionFilter(filters.FilterSet):
    financial_year = filters.CharFilter(
        field_name="financial_year__id", lookup_expr="exact"
    )
    name_np = filters.CharFilter(field_name="name", lookup_expr="icontains")
    name_en = filters.CharFilter(field_name="name_eng", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="exact")
    client_ward = filters.CharFilter(field_name="ward", lookup_expr="exact")
    contract_no = filters.CharFilter(method="filter_by_contract_no")
    operator_ward = filters.ModelChoiceFilter(
        field_name="project__ward", to_field_name="id", queryset=Ward.objects.all()
    )
    work_proposer_type_id = filters.CharFilter(
        field_name="work_proposer_type", lookup_expr="exact"
    )
    pms_level_id = filters.CharFilter(
        field_name="project_level__id", lookup_expr="exact"
    )
    program = filters.CharFilter(field_name="program", lookup_expr="exact")
    subject_area = filters.CharFilter(
        field_name="subject_area__id", lookup_expr="exact"
    )
    start_pms_process = filters.CharFilter(
        field_name="start_pms_process__id", lookup_expr="exact"
    )
    total_cost_amount = filters.NumberFilter(
        field_name="appropriated_amount", lookup_expr="exact"
    )
    total_cost_amount_to = filters.NumberFilter(
        field_name="appropriated_amount", lookup_expr="lte"
    )

    class Meta:
        model = ProjectExecution
        fields = [
            "code",
            "financial_year",
            "ward",
            "work_proposer_type",
            "program",
            "subject_area",
            "start_pms_process",
            "status",
        ]

    def filter_by_contract_no(self, queryset, name, value):
        return queryset.filter(
            id__in=OpeningContractAccount.objects.filter(contract_no=value).values_list(
                "project", flat=True
            )
        )
