from django.urls import path
from rest_framework import routers

from plan_execution.view_classes_and_functions import (
    AccountingTopicViewSet,
    BenefitedDetailViewSet,
    BudgetAllocationDetailViewSet,
    BuildingMaterialDetailViewSet,
    CommentAndOrderViewSet,
    ConsumerFormulationViewSet,
    DepositMandateViewSet,
    EstimationSubmitAcceptanceViewSet,
    ExpenseTypeDetailViewSet,
    InstallmentDetailViewSet,
    InstallmentViewSet,
    InstitutionalCollaborationMandateViewSet,
    MaintenanceArrangementViewSet,
    MeasuringBookViewSet,
    MonitoringCommitteeDetailViewSet,
    NominatedStaffViewSet,
    OfficialProcessApprovalVerificationAPIView,
    OfficialProcessPreparationRequestAPIView,
    OpeningContractAccountViewSet,
    PaymentExitBillViewSet,
    PlanStartDecisionViewSet,
    ProbabilityStudyApproveViewSet,
    ProcessStatusListView,
    ProjectAgreementViewSet,
    ProjectBidCollectionViewSet,
    ProjectCommentLogView,
    ProjectCommentViewSet,
    ProjectDarbhauBidViewSet,
    ProjectDeadlineViewSet,
    ProjectExecutionDocumentViewSet,
    ProjectFinishedBailReturnViewSet,
    ProjectMobilizationViewSet,
    ProjectPhysicalDescriptionViewSet,
    ProjectPreparationLogAPIView,
    ProjectReportFinishedAndUpdateViewSet,
    ProjectRevisionViewSet,
    ProjectTaskViewSet,
    ProjectUnitDetailViewSet,
    RequestSendListView,
    StartPmsProcessViewSet,
    TenderPurchaseBranchViewSet,
    TenderViewSet,
    UserApproveVerificationRequestAPIView,
    UserCommitteeMonitoringViewSet,
    UserCommitteeProjectWorkCompleteViewSet,
)
from plan_execution.views.model_choices_views import (
    BailTypeChoicesView,
    BankGuaranteeTypeChoicesView,
    WorkProposerTypeChoicesView,
)
from plan_execution.views.project_execution_views import ProjectExecutionViewSet
from plan_execution.views.quotation_views import (
    QuotationFirmDetailsViewSet,
    QuotationInvitationForProposalViewSet,
    QuotationSpecificationViewSet,
    QuotationSubmissionApprovalFirmDetailsViewSet,
    QuotationSubmissionApprovalViewSet,
)

router = routers.DefaultRouter()

router.register(
    "project-execution",
    ProjectExecutionViewSet,
    basename="project_execution",
)
router.register(
    "comment-and-orders",
    CommentAndOrderViewSet,
    basename="comment_and_order",
)
router.register(
    "start-pms-process",
    StartPmsProcessViewSet,
    basename="start_pms_process",
)
router.register(
    "plan-start-decision",
    PlanStartDecisionViewSet,
    basename="plan_start_decision",
)
router.register(
    "project-physical-description",
    ProjectPhysicalDescriptionViewSet,
    basename="project_physical_description",
)
router.register(
    "project-execution-document",
    ProjectExecutionDocumentViewSet,
    basename="project_execution_document",
)
router.register(
    "project-unit-detail",
    ProjectUnitDetailViewSet,
    basename="project_unit_detail",
)

router.register(
    "benefited-detail",
    BenefitedDetailViewSet,
    basename="benefited_detail",
)

router.register(
    "project-task",
    ProjectTaskViewSet,
    basename="project_task",
)

router.register(
    "tender-purchase-branch",
    TenderPurchaseBranchViewSet,
    basename="tender_purchase_branch",
)
router.register("accounting-topic", AccountingTopicViewSet, basename="accounting_topic")
router.register("installment", InstallmentViewSet, basename="installment")
router.register(
    "expense-type-detail", ExpenseTypeDetailViewSet, basename="expense_type_detail"
)

router.register(
    "budget-allocation",
    BudgetAllocationDetailViewSet,
    basename="budget_allocation_detail",
)

# इस्टिमेट पेश / स्वीकृत सम्बन्धि
router.register(
    "esa",  # ठेक्कापट्टा, अमानत
    EstimationSubmitAcceptanceViewSet,
    basename="esa",
)
# टेन्डर सम्बन्धि
router.register(
    "tender",
    TenderViewSet,
    basename="tender",
)
# बोलपत्र संकलन
router.register(
    "pbc",
    ProjectBidCollectionViewSet,
    basename="pbc",
)
# दरभाउ पत्र/बोलपत्र स्वीकृत
router.register(
    "pdb",
    ProjectDarbhauBidViewSet,
    basename="pdb",
)
# सम्झौता सम्बन्धि
router.register(
    "agreement",
    ProjectAgreementViewSet,
    basename="agreement",
)
# मोबिलैजेशन
router.register(
    "mobilization",
    ProjectMobilizationViewSet,
    basename="mobilization",
)
# निकासा विल भुक्तानी सम्बन्धि
router.register(
    "peb",
    PaymentExitBillViewSet,
    basename="peb",
)
# म्याद थप
router.register(
    "deadline",
    ProjectDeadlineViewSet,
    basename="deadline",
)
# नापी किताब सम्बन्धि
router.register(
    "measuring-book",
    MeasuringBookViewSet,
    basename="measuring-book",
)
# कार्य सम्पन्न विवरण
router.register(
    "pfbr",
    ProjectFinishedBailReturnViewSet,
    basename="pfbr",
)
router.register(
    "consumer-committee-formulation",
    ConsumerFormulationViewSet,
    basename="consumer_committee_formulation",
)
router.register(
    "probability-study-approve",
    ProbabilityStudyApproveViewSet,
    basename="probability_study_approve",
)
router.register(
    "installment-detail",
    InstallmentDetailViewSet,
    basename="installment_detail",
)
router.register(
    "building-material-detail",
    BuildingMaterialDetailViewSet,
    basename="building_material_detail",
)
router.register(
    "maintenance-arrangement",
    MaintenanceArrangementViewSet,
    basename="maintenance_arrangement",
)
router.register(
    "open-contract-account",
    OpeningContractAccountViewSet,
    basename="open_contract_account",
)
router.register(
    "monitoring-committee-detail",
    MonitoringCommitteeDetailViewSet,
    basename="monitoring_committee_detail",
)
router.register(
    "user-committee-monitoring",
    UserCommitteeMonitoringViewSet,
    basename="user_committee_monitoring",
)
router.register(
    "project-revision",
    ProjectRevisionViewSet,
    basename="project_revision",
)
router.register(
    "user-committee-project-work-complete",
    UserCommitteeProjectWorkCompleteViewSet,
    basename="user_committee_project_work_complete",
)
router.register(
    "deposit-mandate",
    DepositMandateViewSet,
    basename="deposit_mandate",
)

router.register(
    "nominated-staff",
    NominatedStaffViewSet,
    basename="nominated_staff",
)

router.register(
    "institutional-collaboration-mandate",
    InstitutionalCollaborationMandateViewSet,
    basename="institutional_collaboration_mandate",
)

router.register(
    "project-report-finish-and-update",
    ProjectReportFinishedAndUpdateViewSet,
    basename="project_report_finish_and_update",
)
router.register(
    "project-comment",
    ProjectCommentViewSet,
    basename="project_comment",
)
# Quotatton ViewSets
router.register(
    "quotation_firm_details",
    QuotationFirmDetailsViewSet,
    basename="quotation_firm_details",
)
router.register(
    "quotation_specification",
    QuotationSpecificationViewSet,
    basename="quotation_specification",
)
router.register(
    "quot_sa_firm_details",
    QuotationSubmissionApprovalFirmDetailsViewSet,
    basename="submission_approval_firm_details",
)
router.register(
    "ifp",
    QuotationInvitationForProposalViewSet,
    basename="ifp",
)
router.register(
    "submission_approval",
    QuotationSubmissionApprovalViewSet,
    basename="submission_approval",
)

urlpatterns = router.urls

model_choices_urls = [
    path(
        "work-proposer-type/",
        WorkProposerTypeChoicesView.as_view(),
        name="work_proposer_type",
    ),
    path(
        "bank-guarantee-type/",
        BankGuaranteeTypeChoicesView.as_view(),
        name="bank_guarantee_type",
    ),
    path(
        "bail-type/",
        BailTypeChoicesView.as_view(),
        name="bail_type",
    ),
]

other_urls = [
    path(
        "official-process-preparation-request/",
        OfficialProcessPreparationRequestAPIView.as_view(),
        name="official_process_preparation_request",
    ),
    path(
        "official-process-approval-verification/<int:preparation_id>/",
        OfficialProcessApprovalVerificationAPIView.as_view(),
        name="approval-verification-process",
    ),
    path(
        "approval-verification-requests/<int:project_id>/",
        UserApproveVerificationRequestAPIView.as_view(),
        name="approval-verification-requests",
    ),
    path(
        "offcial-process-log/<int:project_id>/",
        ProjectPreparationLogAPIView.as_view(),
        name="official-process-log",
    ),
    path(
        "process-status/", ProcessStatusListView.as_view(), name="process-status-list"
    ),
    path("request-send-for/", RequestSendListView.as_view(), name="request-send-list"),
    path(
        "project-comment-log/<int:project_id>/",
        ProjectCommentLogView.as_view(),
        name="project-comment-log",
    ),
]

urlpatterns += model_choices_urls
urlpatterns += other_urls
