import logging as logger
import random

from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from base_model.viewsets import (
    ChildCreationSupportViewSet,
    MultipleObjectSupportViewSet,
    MunicipalityAndProjectFilteredViewSet,
)
from notification.models import Notification
from plan_execution.choices import ProcessNameChoices
from plan_execution.filters import (
    BudgetAllocationDetailFilter,
    ProjectInstallmentFilter,
)
from plan_execution.models import (
    AccountingTopic,
    BailType,
    BenefitedDetail,
    BudgetAllocationDetail,
    BuildingMaterialDetail,
    CommentAndOrder,
    ConsumerFormulation,
    DepositMandate,
    EstimationSubmitAcceptance,
    ExpenseTypeDetail,
    InstallmentDetail,
    InstitutionalCollaborationMandate,
    InstitutionalCollaborationNominatedStaff,
    MaintenanceArrangement,
    MeasuringBook,
    MonitoringCommitteeDetail,
    OfficialProcess,
    OpeningContractAccount,
    PaymentDetail,
    PaymentExitBill,
    PlanStartDecision,
    ProbabilityStudyApprove,
    ProjectAgreement,
    ProjectBidCollection,
    ProjectComment,
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
    PSABuildingMaterial,
    StartPmsProcess,
    TenderPurchaseBranch,
    UserCommitteeMonitoring,
    UserCommitteeProjectWorkComplete,
)
from plan_execution.serializers import (
    AccountingTopicSerializer,
    ApprovalVerificationSerializer,
    BailTypeSerializer,
    BenefitedDetailSerializer,
    BudgetAllocationDetailSerializer,
    BuildingMaterialDetailSerializer,
    CommentAndOrderSerializer,
    ConstantSerializer,
    ConsumerFormulationSerializer,
    DepositMandateSerializer,
    EstimationSubmitAcceptanceSerializer,
    ExpenseTypeDetailSerializer,
    InstallmentDetailSerializer,
    InstallmentSerializer,
    InstitutionalCollaborationMandateSerializer,
    MaintenanceArrangementSerializer,
    MeasuringBookSerializer,
    MonitoringCommitteeDetailSerializer,
    NominatedStaffSerializer,
    OfficialProcessLogSerializer,
    OfficialProcessRequestSerializer,
    OpeningContractAccountSerializer,
    PaymentDetailSerializer,
    PaymentExitBillSerializer,
    PlanStartDecisionSerializer,
    ProbabilityStudyApproveSerializer,
    ProjectAgreementSerializer,
    ProjectBidCollectionSerializer,
    ProjectCommentSerializer,
    ProjectDarbhauBidSerializer,
    ProjectDeadlineSerializer,
    ProjectExecutionDocumentSerializer,
    ProjectFinishedBailReturnSerializer,
    ProjectMobilizationDetailSerializer,
    ProjectMobilizationSerializer,
    ProjectPhysicalDescriptionSerializer,
    ProjectReportFinishedAndUpdateSerializer,
    ProjectRevisionSerializer,
    ProjectTaskSerializer,
    ProjectUnitDetailSerializer,
    PSABuildingMaterialSerializer,
    StartPmsProcessSerializer,
    TenderPurchaseBranchSerializer,
    TenderSerializer,
    UserCommitteeMonitoringSerializer,
    UserCommitteeProjectWorkCompleteSerializer,
)
from pms_system import settings
from project.models import Project
from project_planning.models import (
    AccountTitleManagement,
    BudgetSource,
    BudgetSubTitle,
    ProjectType,
    SubjectArea,
)
from project_planning.serializers import ATMSerializer
from utils.constants import (
    BANK_GUARANTEE_TYPE,
    WORK_PROPOSER_TYPE,
    ProcessStatus,
    RequestSend,
)
from utils.extract_budget_from_excel import extract_data_from_four_quarters_excel
from utils.nepali_nums import english_nums

# Create your views here.


class StartPmsProcessViewSet(ModelViewSet):
    serializer_class = StartPmsProcessSerializer
    queryset = StartPmsProcess.objects.all()


class PlanStartDecisionViewSet(ModelViewSet):
    serializer_class = PlanStartDecisionSerializer
    queryset = PlanStartDecision.objects.all()


class WorkProposerTypeViewSet(APIView):
    def get(self, request, *args, **kwargs):
        try:
            print("Getting work process type from constants")
            response = {
                "results": [
                    {
                        "code": item[0],
                        "name": item[1],
                    }
                    for item in WORK_PROPOSER_TYPE
                ]
            }
            return Response(response)
        except Exception as e:
            print("Expense determine level data: {e}")
            return False


class ProjectPhysicalDescriptionViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectPhysicalDescriptionSerializer
    model = ProjectPhysicalDescription
    project_required = True


class ProjectExecutionDocumentViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectExecutionDocumentSerializer
    model = ProjectExecutionDocument
    project_required = True


class ProjectUnitDetailViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectUnitDetailSerializer
    model = ProjectUnitDetail
    project_required = True


class BudgetAllocationDetailViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = BudgetAllocationDetailSerializer
    queryset = BudgetAllocationDetail.objects.all()
    model = BudgetAllocationDetail
    project_required = True
    filterset_class = BudgetAllocationDetailFilter

    @action(detail=False, methods=["post"])
    def import_excel(self, request, *args, **kwargs):
        excel_file = request.FILES.get("excel_file")
        if excel_file is None:
            return Response(
                {"success": False, "message": "Please select excel file."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        amount_is_thousands = request.data.get("amount_is_thousands", False)
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
        for budget_sub_title_name, budget_allocation_details in budget_data.items():
            bst_code = budget_sub_title_name.split(" ")[0].strip()
            (
                budget_sub_title,
                budget_sub_title_created,
            ) = BudgetSubTitle.objects.get_or_create(
                code=bst_code,
                name=budget_sub_title_name,
            )
            for budget_allocation_detail in budget_allocation_details:
                budget_allocation_creation_data = {
                    "budget_sub_title": budget_sub_title,
                }
                # Getting Budget Source
                (
                    budget_source,
                    budget_source_created,
                ) = BudgetSource.objects.get_or_create(
                    name=budget_allocation_detail["source"]
                )
                budget_allocation_creation_data["budget_source"] = budget_source
                # Getting Budget Allocation Expense Title
                (
                    expense_title,
                    expense_title_created,
                ) = AccountTitleManagement.objects.get_or_create(
                    code=str(budget_allocation_detail["expense_title"]),
                )
                budget_allocation_creation_data["expense_title"] = expense_title
                # Getting Budget Amounts
                budget_allocation_creation_data["first_quarter"] = (
                    budget_allocation_detail["allocation"]["first_quarter"]
                )
                budget_allocation_creation_data["second_quarter"] = (
                    budget_allocation_detail["allocation"]["second_quarter"]
                )
                budget_allocation_creation_data["third_quarter"] = (
                    budget_allocation_detail["allocation"]["third_quarter"]
                )
                budget_allocation_creation_data["fourth_quarter"] = (
                    budget_allocation_detail["allocation"]["fourth_quarter"]
                )
                budget_allocation_creation_data["total"] = budget_allocation_detail[
                    "allocation"
                ]["total"]
                # Getting Subject Area
                (
                    subject_area,
                    subject_area_created,
                ) = SubjectArea.objects.get_or_create(
                    name=budget_allocation_detail["sub_topic"]
                )
                budget_allocation_creation_data["subject_area"] = subject_area
                # Creating Project
                project = Project.objects.create(
                    name=budget_allocation_detail["project_name"],
                    municipality=request.user.assigned_municipality,
                )
                # Creating Project Execution
                project_execution = ProjectExecution.objects.create(
                    project=project,
                    subject_area=subject_area,
                )
                budget_allocation_creation_data["project"] = project_execution
                # Getting project year
                budget_allocation_creation_data["multi_year_budget"] = (
                    int(english_nums(budget_allocation_detail["target"])) > 1
                )

                BudgetAllocationDetail.objects.create(**budget_allocation_creation_data)

        return Response(
            {"success": True, "message": "Data imported successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def ebudgeting_details(self, request, *args, **kwargs):
        expense_titles_queryset = AccountTitleManagement.objects.filter(
            module__name_eng="Expenditure"
        ).prefetch_related(
            "allocated_budget_details",
        )
        ebudgeting_details_response = []
        for expense_title in expense_titles_queryset:
            expense_ebudgeting_data = {}
            expense_title_serializer = ATMSerializer(expense_title)
            expense_ebudgeting_data["expense_title"] = expense_title_serializer.data
            budget_allocation_details_serializer = BudgetAllocationDetailSerializer(
                expense_title.allocated_budget_details.all(), many=True
            )
            expense_ebudgeting_data["budget_allocation_details"] = (
                budget_allocation_details_serializer.data
            )
            expense_ebudgeting_data["estimated_expenditure_amount"] = (
                expense_title.estimated_expenditure_amount
            )
            expense_ebudgeting_data["revised_expenditure_amount"] = (
                expense_title.revised_expenditure_amount
            )
            ebudgeting_details_response.append(expense_ebudgeting_data)
        return Response(ebudgeting_details_response)

    @action(detail=False, methods=["get"])
    def expense_titles(self, request, *args, **kwargs):
        expense_titles_queryset = AccountTitleManagement.objects.filter(
            module__name_eng="Expenditure"
        )
        expense_titles_serializer = ATMSerializer(expense_titles_queryset, many=True)
        return Response(expense_titles_serializer.data)


class BenefitedDetailViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = BenefitedDetailSerializer
    model = BenefitedDetail
    project_required = True


class ProjectTaskViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectTaskSerializer
    model = ProjectTask
    project_required = True


class TenderPurchaseBranchViewSet(ModelViewSet):
    serializer_class = TenderPurchaseBranchSerializer
    queryset = TenderPurchaseBranch.objects.all()


class BankGuaranteeTypeView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            response = {item[1]: item[0] for item in BANK_GUARANTEE_TYPE}
            return Response(response)
        except Exception as e:
            print("Expense determine level data: {e}")
            return False


class BailTypeViewSet(ModelViewSet):
    serializer_class = BailTypeSerializer
    queryset = BailType.objects.all()


class AccountingTopicViewSet(ModelViewSet):
    serializer_class = AccountingTopicSerializer
    queryset = AccountingTopic.objects.all()


class InstallmentViewSet(ModelViewSet):
    serializer_class = InstallmentSerializer
    queryset = ProjectInstallment.objects.all()
    filterset_class = ProjectInstallmentFilter


class ExpenseTypeDetailViewSet(ModelViewSet):
    serializer_class = ExpenseTypeDetailSerializer
    queryset = ExpenseTypeDetail.objects.all()


class EstimationSubmitAcceptanceViewSet(MunicipalityAndProjectFilteredViewSet):
    """
    इस्टिमेट पेश / स्वीकृत सम्बन्धि
    """

    serializer_class = EstimationSubmitAcceptanceSerializer
    model = EstimationSubmitAcceptance
    project_required = True
    return_only_one = True
    is_project_process = True
    block_multiple_object_creation = True
    send_data_directly = True


class TenderViewSet(MunicipalityAndProjectFilteredViewSet):
    """
    टेन्डर सम्बन्धि
    """

    serializer_class = TenderSerializer
    model = ProjectTender
    project_required = True
    return_only_one = True
    is_project_process = True
    block_multiple_object_creation = True
    send_data_directly = True


class ProjectBidCollectionViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectBidCollectionSerializer
    model = ProjectBidCollection
    project_required = True


class ProjectDarbhauBidViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectDarbhauBidSerializer
    model = ProjectDarbhauBid
    project_required = True
    is_project_process = True
    block_multiple_object_creation = True
    return_only_one = True
    send_data_directly = True


class ProjectAgreementViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectAgreementSerializer
    model = ProjectAgreement
    project_required = True
    is_project_process = True
    block_multiple_object_creation = True
    return_only_one = True
    send_data_directly = True


class ProjectMobilizationViewSet(ChildCreationSupportViewSet):
    serializer_class = ProjectMobilizationSerializer
    model = ProjectMobilization
    project_required = True
    child_payload_properties = [
        {
            "model": ProjectMobilizationDetail,
            "serializer_class": ProjectMobilizationDetailSerializer,
            "child_name": "mobilization_details",
            "parent_name": "mobilization",
        }
    ]
    return_only_one = True
    is_project_process = True
    block_multiple_object_creation = True


class PaymentExitBillViewSet(ChildCreationSupportViewSet):
    serializer_class = PaymentExitBillSerializer
    model = PaymentExitBill
    project_required = True
    block_deleting_if_used_in_relation = False
    child_payload_properties = [
        {
            "model": PaymentDetail,
            "serializer_class": PaymentDetailSerializer,
            "child_name": "payment_details",
            "parent_name": "peb",
        }
    ]
    is_project_process = True


class ProjectDeadlineViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectDeadlineSerializer
    model = ProjectDeadline
    project_required = True

    # foreign_key_fields = [
    #     {
    #         "field_name_in_model": "decision_by",
    #         "pk_field_name": "id",
    #     },
    #     {
    #         "field_name_in_model": "project",
    #         "pk_field_name": "id",
    #     },
    # ]

    # def create(self, request, *args, **kwargs):
    #     try:
    #         request_data = request.data
    #         create = request_data.pop("new")
    #         update = request_data.pop("updated")
    #         delete = request_data.pop("deleted")
    #         status = False
    #         if create and len(create) > 0:
    #             status = self.perform_create(create)
    #         if update and len(update) > 0:
    #             status = self.perform_update(update)
    #         if delete and len(delete) > 0:
    #             status = self.delete_objects(delete)
    #         if status:
    #             return Response(status=200)
    #         return Response(status=204)
    #     except Exception as e:
    #         print("Exception", e, 999999999)
    #         return Response(status=204)
    #
    # def delete_objects(self, deleted_data):
    #     try:
    #         for data in deleted_data:
    #             print(data["id"], 7238798172398)
    #             instance = ProjectDeadline.objects.filter(id=data["id"]).first()
    #             instance.delete()
    #         return True
    #     except Exception as e:
    #         logger.exception(f"Exception: {e}")
    #         return False
    #
    # def perform_create(self, serializer):
    #     try:
    #         result = []
    #         serializer = self.get_serializer(data=serializer, many=True)
    #         serializer.is_valid(raise_exception=True)
    #         instances = serializer.save()
    #         serialized_data = self.serializer_class(instances, many=True).data
    #         result.append(serialized_data)
    #         return True
    #     except Exception as e:
    #         logger.exception(f"Create instance, {e}")
    #         return False
    #
    # def perform_update(self, update_date):
    #     try:
    #         instances = []
    #         for data in update_date:
    #             instance = ProjectDeadline.objects.get(id=data["id"])
    #             serializer = self.get_serializer(instance, data=data, partial=True)
    #             serializer.is_valid(raise_exception=True)
    #             serializer = serializer.save()
    #             # instances.append(serializer.instance)
    #         return instances
    #     except Exception as e:
    #         logger.exception(f"Exception: {e}")
    #         return False


class MeasuringBookViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = MeasuringBookSerializer
    model = MeasuringBook
    project_required = True


class ProjectFinishedBailReturnViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectFinishedBailReturnSerializer
    model = ProjectFinishedBailReturn
    project_required = True
    return_only_one = True
    is_project_process = True
    block_multiple_object_creation = True
    send_data_directly = True


class ConsumerFormulationViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ConsumerFormulationSerializer
    model = ConsumerFormulation


class ProbabilityStudyApproveViewSet(ChildCreationSupportViewSet):
    serializer_class = ProbabilityStudyApproveSerializer
    model = ProbabilityStudyApprove
    child_payload_properties = [
        {
            "model": PSABuildingMaterial,
            "serializer_class": PSABuildingMaterialSerializer,
            "child_name": "materials",
            "parent_name": "probability_study_approve",
        },
    ]
    is_project_process = True
    block_multiple_object_creation = True
    return_only_one = True


class InstallmentDetailViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = InstallmentDetailSerializer
    model = InstallmentDetail


class BuildingMaterialDetailViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = BuildingMaterialDetailSerializer
    model = BuildingMaterialDetail


class MaintenanceArrangementViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = MaintenanceArrangementSerializer
    model = MaintenanceArrangement


class OpeningContractAccountViewSet(ChildCreationSupportViewSet):
    serializer_class = OpeningContractAccountSerializer
    model = OpeningContractAccount
    child_payload_properties = [
        {
            "model": InstallmentDetail,
            "serializer_class": InstallmentDetailSerializer,
            "child_name": "installment",
            "parent_name": "opening_contract_account",
        },
        {
            "model": BuildingMaterialDetail,
            "serializer_class": BuildingMaterialDetailSerializer,
            "child_name": "materials",
            "parent_name": "opening_contract_account",
        },
        {
            "model": MaintenanceArrangement,
            "serializer_class": MaintenanceArrangementSerializer,
            "child_name": "maintenance",
            "parent_name": "opening_contract_account",
        },
    ]
    is_project_process = True
    block_multiple_object_creation = True
    return_only_one = True


class MonitoringCommitteeDetailViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = MonitoringCommitteeDetailSerializer
    model = MonitoringCommitteeDetail


class UserCommitteeMonitoringViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = UserCommitteeMonitoringSerializer
    model = UserCommitteeMonitoring
    project_required = True
    return_only_one = True
    is_project_process = True
    block_multiple_object_creation = True


class CommentAndOrderViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = CommentAndOrderSerializer
    model = CommentAndOrder
    project_required = True
    return_only_one = True
    is_project_process = True
    block_multiple_object_creation = True


class ProjectRevisionViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectRevisionSerializer
    model = ProjectRevision


class UserCommitteeProjectWorkCompleteViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = UserCommitteeProjectWorkCompleteSerializer
    model = UserCommitteeProjectWorkComplete
    project_required = True
    return_only_one = True
    is_project_process = True
    block_multiple_object_creation = True


class DepositMandateViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = DepositMandateSerializer
    model = DepositMandate


class NominatedStaffViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = NominatedStaffSerializer
    model = InstitutionalCollaborationNominatedStaff


class InstitutionalCollaborationMandateViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = InstitutionalCollaborationMandateSerializer
    model = InstitutionalCollaborationMandate


class ProjectReportFinishedAndUpdateViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = ProjectReportFinishedAndUpdateSerializer
    model = ProjectReportFinishedAndUpdate


class ProjectPreparationLogAPIView(GenericAPIView):
    serializer_class = OfficialProcessLogSerializer

    def get(self, request, *args, **kwargs):
        try:
            context = {}
            project_id = self.kwargs.get("project_id")
            preparation_log = OfficialProcess.objects.filter(
                project__id=project_id
            ).order_by("-created_date")
            if preparation_log:
                preparation_log_serializer = OfficialProcessLogSerializer(
                    preparation_log, many=True
                )
                context["official_process_log"] = preparation_log_serializer.data
                context["project"] = project_id

            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            raise e


class OfficialProcessPreparationRequestAPIView(GenericAPIView):
    serializer_class = OfficialProcessRequestSerializer
    queryset = OfficialProcess.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            serializer = OfficialProcessRequestSerializer(data=request.data)
            if serializer.is_valid():
                request_by = serializer.validated_data["request_by"]
                send_to = serializer.validated_data["send_to"]
                send_for = serializer.validated_data["send_for"]
                remarks = serializer.validated_data.get("remarks")
                file = serializer.validated_data.get("file")
                project = serializer.validated_data["project"]
                user_official_process = OfficialProcess.objects.filter(
                    project=project, send_to=send_to, status="P"
                ).first()

                if user_official_process:
                    serializer_data = OfficialProcessLogSerializer(
                        user_official_process
                    )
                    return Response(
                        data=serializer_data.data, status=status.HTTP_400_BAD_REQUEST
                    )
                preparation_process = OfficialProcess.objects.create(
                    request_by=request_by,
                    send_to=send_to,
                    send_for=send_for,
                    remarks=remarks,
                    file=file,
                    project=project,
                )
                # notification
                request_type = dict(RequestSend.choices)[send_for]
                full_name = f"{request_by.first_name} {request_by.last_name}"
                Notification.objects.create(
                    title=f"Project {project.code}-{project.name} {request_type} request ",
                    description=f"Project {project.code}-{project.name} request for {request_type} by {full_name}.",
                    project=project,
                    official_process=preparation_process,
                    user=send_to,
                    link=f"{settings.SITE_HOST}/api/approval-verification-requests/{project.id}/",
                )
                print("Notification send successfully.")
                serializer_data = OfficialProcessRequestSerializer(preparation_process)
                return Response(
                    data=serializer_data.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    "success": False,
                    "message": f"Invalid data input, {serializer.errors}",
                }
            )
        except Exception as e:
            return Response(
                {"success": False, "message": f"{e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class OfficialProcessApprovalVerificationAPIView(GenericAPIView):
    serializer_class = ApprovalVerificationSerializer
    queryset = OfficialProcess.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            serializer = ApprovalVerificationSerializer(data=request.data)
            preparation_id = self.kwargs.get("preparation_id")

            if serializer.is_valid():
                process_status = serializer.validated_data["status"]
                feedback_remarks = serializer.validated_data.get("feedback_remarks")
                feedback_file = serializer.validated_data.get("feedback_file")
                project = serializer.validated_data["project"]

                preparation_process = OfficialProcess.objects.filter(
                    id=preparation_id, project=project
                ).first()
                if preparation_process:
                    preparation_process.status = process_status
                    preparation_process.feedback_remarks = feedback_remarks
                    preparation_process.feedback_file = feedback_file
                    preparation_process.project = project
                    preparation_process.save()
                    # project = ProjectExecution.objects.filter(id=project_id).first()
                    send_for = preparation_process.send_for
                    request_type = dict(RequestSend.choices)[send_for]
                    status_type = dict(ProcessStatus.choices)[
                        preparation_process.status
                    ]
                    full_name = f"{request.user.first_name} {request.user.last_name}"
                    Notification.objects.create(
                        title=f"Project {project.code}-{project.name} {request_type} request {status_type}",
                        description=f"Project {project.code}-{project.name}, {request_type} request is {status_type} "
                        f"by {full_name}.",
                        project=project,
                        official_process=preparation_process,
                        link=f"{settings.SITE_HOST}/api/approval-verification-requests/{project.id}/",
                        user=preparation_process.request_by,
                    )
                    serializer = ApprovalVerificationSerializer(preparation_process)
                    return Response(
                        serializer.data,
                        status=status.HTTP_200_OK,
                    )
            return Response(
                {"success": False, "message": f"Unable to update official process."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": f"{e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserApproveVerificationRequestAPIView(GenericAPIView):
    serializer_class = OfficialProcessLogSerializer

    def get(self, request, *args, **kwargs):
        try:
            context = {}
            project_id = self.kwargs.get("project_id")
            user = request.user
            preparation_log = OfficialProcess.objects.filter(
                project__id=project_id, send_to=user, status="P"
            )
            if preparation_log:
                preparation_log_serializer = OfficialProcessLogSerializer(
                    preparation_log, many=True
                )
                context["official_process_log"] = preparation_log_serializer.data
                context["project"] = project_id

            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            raise e


class ProcessStatusListView(APIView):
    def get(self, request):
        choices = [
            {"value": choice[0], "label": choice[1]} for choice in ProcessStatus.choices
        ]
        serializer = ConstantSerializer(choices, many=True)
        return Response(serializer.data)


class RequestSendListView(APIView):
    def get(self, request):
        choices = [
            {"value": choice[0], "label": choice[1]} for choice in RequestSend.choices
        ]
        serializer = ConstantSerializer(choices, many=True)
        return Response(serializer.data)


class ProjectCommentViewSet(ModelViewSet):
    serializer_class = ProjectCommentSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get("project_id")
        queryset = ProjectComment.objects.all()
        if project_id:
            queryset = queryset.filter(project__id=project_id)
        return queryset

    @action(detail=False, methods=["get"])
    def process_names(self, request: HttpRequest):
        process_names = [
            {"value": choice[0], "label": choice[1]}
            for choice in ProcessNameChoices.choices
        ]
        return Response(process_names)


class ProjectCommentLogView(APIView):
    def get(self, request: HttpRequest, project_id: int):
        queryset = ProjectComment.objects.filter(project__id=project_id).order_by(
            "-created_date"
        )
        serializer = ProjectCommentSerializer(
            queryset, context={"request": request}, many=True
        )
        return Response(serializer.data)
