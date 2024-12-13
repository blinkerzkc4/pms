import logging

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from budget_process.models import (
    BudgetAmmendment,
    BudgetExpenseManagement,
    BudgetManagement,
    BudgetTransfer,
    EstimateFinancialArrangements,
    ExpenseBudgetRangeDetermine,
    IncomeBudgetRangeDetermine,
    BudgetImportLog,
)
from budget_process.serializers import (
    BudgetAmmendmentSerializer,
    BudgetExpenseManagementSerializer,
    BudgetManagementSeralizer,
    BudgetTransferSerializer,
    EFACreateSerializer,
    EFAViewSerializer,
    ExpenseRangeDetermineCreateSerializer,
    ExpenseRangeDetermineViewSerializer,
    IncomeRangeDetermineCreateSerializer,
    IncomeRangeDetermineViewSerializer,
)
from plan_execution.models import BudgetAllocationDetail, ProjectExecution
from project.models import FinancialYear, Project
from project_planning.filters import (
    BudgetAmmendmentFilter,
    BudgetExpenseManagementFilter,
    BudgetManagementFilter,
    BudgetTransferFilter,
    EstimateFinancialArrangementsFilter,
    ExpenseBudgetRangeDetermineFilter,
    IncomeBudgetRangeDetermineFilter,
)
from project_planning.models import (
    AccountTitleManagement,
    BudgetSource,
    SubjectArea,
    SubModule,
)
from project_planning.serializers import ATMSerializer
from utils.constants import EXPENSE_DETERMINE_LEVEL
from utils.extract_budget_from_excel import extract_data_from_four_quarters_excel
from utils.nepali_nums import english_nums

# Create your views here.
logger = logging.getLogger("Budget process")


class ExpenseDetermineLevelViewSet(APIView):
    def get(self, request, *args, **kwargs):
        try:
            logger.info("Expense determine level data getting.")
            response = {item[1]: item[0] for item in EXPENSE_DETERMINE_LEVEL}
            return Response(response)
        except Exception as e:
            print("Expense determine level data: {e}")
            return False


class ExpenseBudgetRangeDetermineViewSet(ModelViewSet):
    serializer_class = ExpenseRangeDetermineCreateSerializer
    queryset = ExpenseBudgetRangeDetermine.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseBudgetRangeDetermineFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ExpenseRangeDetermineViewSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        expense_determine_level = self.request.query_params.get(
            "expense_determine_level"
        )
        is_budget_estimates = self.request.query_params.get("is_budget_estimates")
        queryset = ExpenseBudgetRangeDetermine.objects.all()
        if is_budget_estimates:
            queryset = queryset.filter(is_budget_estimates=True)
        elif expense_determine_level == "ward":
            queryset = queryset.filter(is_budget_estimates=False).exclude(ward=None)
        else:
            queryset = queryset.filter(is_budget_estimates=False, ward=None)
        print(queryset, 98798798)
        serializer = ExpenseRangeDetermineViewSerializer(queryset, many=True)
        response_data = {
            "count": len(serializer.data),
            "next": None,
            "previous": None,
            "results": serializer.data,
        }
        return Response(response_data)


class IncomeBudgetRangeDetermineViewSet(ModelViewSet):
    serializer_class = IncomeRangeDetermineCreateSerializer
    queryset = IncomeBudgetRangeDetermine.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = IncomeBudgetRangeDetermineFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = IncomeRangeDetermineViewSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = IncomeRangeDetermineViewSerializer(queryset, many=True)
        response_data = {
            "count": len(serializer.data),
            "next": None,
            "previous": None,
            "results": serializer.data,
        }
        return Response(response_data)


class EFAViewSet(ModelViewSet):
    serializer_class = EFACreateSerializer
    queryset = EstimateFinancialArrangements.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstimateFinancialArrangementsFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EFAViewSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = EFAViewSerializer(queryset, many=True)
        response_data = {
            "count": len(serializer.data),
            "next": None,
            "previous": None,
            "results": serializer.data,
        }
        return Response(response_data)


class BudgetExpenseManagementViewSet(ModelViewSet):
    serializer_class = BudgetExpenseManagementSerializer
    queryset = BudgetExpenseManagement.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BudgetExpenseManagementFilter

    @action(detail=False, methods=["get"])
    def import_template(self, request, *args, **kwargs):
        with open("samples/budget_import_sample.xlsx", "rb") as excel_file:
            response = HttpResponse(
                excel_file.read(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = (
                "attachment; filename=" + "budget_import_template.xlsx"
            )
            return response

    @action(detail=False, methods=["post"])
    def import_excel(self, request, *args, **kwargs):
        excel_file = request.FILES.get("excel_file")
        amount_is_thousands = request.data.get("amount_is_thousands", False)

        if isinstance(amount_is_thousands, str):
            amount_is_thousands = amount_is_thousands == "true"

        if excel_file is None:
            return Response(
                {"success": False, "message": "Please select excel file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.data.get("financial_year"):
            financial_year = FinancialYear.objects.get(
                id=int(request.data.get("financial_year"))
            )
        else:
            financial_year = FinancialYear.current_fy()
        try:
            budget_data = extract_data_from_four_quarters_excel(
                excel_file, amount_is_thousands
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {
                    "success": False,
                    "message": "Excel format doesn't match the requirements.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Creating Import Log
        import_payload = request.data.copy()
        import_payload.pop("excel_file")
        budget_import_log = BudgetImportLog.objects.create(
            created_by=request.user,
            imported_file=excel_file,
            import_payload=import_payload,
        )

        for (
            sub_module_name,
            budget_expense_management_data_list,
        ) in budget_data.items():
            sub_module, created = SubModule.objects.get_or_create(name=sub_module_name)
            for budget_expense_management_data in budget_expense_management_data_list:
                budget_expense_management_creation_data = {
                    "sub_module": sub_module,
                    "financial_year": financial_year,
                }
                (
                    budget_source,
                    budget_source_created,
                ) = BudgetSource.objects.get_or_create(
                    name=budget_expense_management_data["source"]
                )
                budget_expense_management_creation_data["budget_source"] = budget_source
                # Getting Budget Allocation Expense Title
                (
                    expense_title,
                    expense_title_created,
                ) = AccountTitleManagement.objects.get_or_create(
                    code=str(budget_expense_management_data["expense_title"]),
                )
                budget_expense_management_creation_data["expense_title"] = expense_title
                # Getting Budget Amounts
                budget_expense_management_creation_data[
                    "first_quarter"
                ] = budget_expense_management_data["allocation"]["first_quarter"]
                budget_expense_management_creation_data[
                    "second_quarter"
                ] = budget_expense_management_data["allocation"]["second_quarter"]
                budget_expense_management_creation_data[
                    "third_quarter"
                ] = budget_expense_management_data["allocation"]["third_quarter"]
                budget_expense_management_creation_data[
                    "forth_quarter"
                ] = budget_expense_management_data["allocation"]["fourth_quarter"]
                budget_expense_management_creation_data[
                    "estimated_expense_amount"
                ] = budget_expense_management_data["allocation"]["total"]
                # Getting Subject Area
                (
                    subject_area,
                    subject_area_created,
                ) = SubjectArea.objects.get_or_create(
                    name=budget_expense_management_data["sub_topic"]
                )
                budget_expense_management_creation_data["subject_area"] = subject_area
                budget_expense_management_creation_data["aim"] = int(
                    english_nums(budget_expense_management_data["target"])
                )
                budget_expense_management_creation_data[
                    "unit"
                ] = budget_expense_management_data["unit"]
                budget_expense_management_creation_data[
                    "activity_name"
                ] = budget_expense_management_data["activity_name"]
                budget_expense_management_creation_data[
                    "municipality"
                ] = request.user.assigned_municipality

                budget_expense_management = BudgetExpenseManagement.objects.create(
                    **budget_expense_management_creation_data
                )
                budget_import_log.imported_bem.add(budget_expense_management)

        return Response(
            {"success": True, "message": "Budget imported successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def ebudgeting_details(self, request, *args, **kwargs):
        filter_kwargs = {
            "module__name_eng": "Expenditure",
        }

        if request.query_params.get("parent"):
            filter_kwargs["id"] = request.query_params.get("parent")

        expense_titles_queryset = AccountTitleManagement.objects.filter(
            **filter_kwargs
        ).prefetch_related(
            "budget_expenses",
        )
        ebudgeting_details_response = []
        for expense_title in expense_titles_queryset:
            expense_ebudgeting_data = {}
            expense_title_serializer = ATMSerializer(expense_title)
            expense_ebudgeting_data["expense_title"] = expense_title_serializer.data
            budget_expenses_serializer = BudgetExpenseManagementSerializer(
                expense_title.budget_expenses.all(), many=True
            )
            expense_ebudgeting_data["budget_expenses"] = budget_expenses_serializer.data
            expense_ebudgeting_data[
                "estimated_expenditure_amount"
            ] = expense_title.estimated_expenditure_amount
            expense_ebudgeting_data[
                "revised_expenditure_amount"
            ] = expense_title.revised_expenditure_amount
            ebudgeting_details_response.append(expense_ebudgeting_data)
        return Response(ebudgeting_details_response)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = EFAViewSerializer(instance)
    #     return Response(serializer.data)
    #
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = EFAViewSerializer(queryset, many=True)
    #     return Response(serializer.data)


class BudgetTransferViewSet(ModelViewSet):
    serializer_class = BudgetTransferSerializer
    queryset = BudgetTransfer.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BudgetTransferFilter


class BudgetAmmendmentViewSet(ModelViewSet):
    serializer_class = BudgetAmmendmentSerializer
    queryset = BudgetAmmendment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BudgetAmmendmentFilter


class BudgetManagementViewSet(ModelViewSet):
    serializer_class = BudgetManagementSeralizer
    queryset = BudgetManagement.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BudgetManagementFilter
