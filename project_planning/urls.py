"""
-- Created by Bikash Saud
--
-- Created on 2023-06-07
"""
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register("district", views.DistrictViewSet, basename="district")
router.register("subject-area", views.SubjectAreaViewSet, basename="subject_area")
router.register("bank-type", views.BankTypeViewSet, basename="bank_type")
router.register("payment-medium", views.PaymentMediumViewSet, basename="payment_medium")
router.register("cheque-format", views.ChequeFormatViewSet, basename="cheque_format")
router.register("bfi", views.BFIViewSet, basename="bfi")
router.register("bank-account", views.BankAccountViewSet, basename="bank_account")
router.register(
    "organization-type", views.OrganizationTypeViewSet, basename="organization_type"
)
router.register("organization", views.OrganizationViewSet, basename="organization")
router.register("member-type", views.MemberTypeViewSet, basename="member_type")
router.register(
    "consumer-committee-documents",
    views.ConsumerCommitteeDocumentViewSet,
    basename="consumer_committee_documents",
)
router.register(
    "consumer-committee-members",
    views.ConsumerCommitteeMemberViewSet,
    basename="consumer_committee_members",
)
router.register(
    "consumer-committee", views.ConsumerCommitteeViewSet, basename="consumer_committee"
)
router.register(
    "monitoring-committee-documents",
    views.MonitoringCommitteeDocumentViewSet,
    basename="monitoring_committee_documents",
)
router.register(
    "monitoring-committee-members",
    views.MonitoringCommitteeMemberViewSet,
    basename="monitoring_committee_members",
)
router.register(
    "monitoring-committee",
    views.MonitoringCommitteeViewSet,
    basename="monitoring_committee",
)
router.register(
    "executive-agency", views.ExecutiveAgencyViewSet, basename="executive_agency"
)
router.register("expense-type", views.ExpanseTypeViewSet, basename="expense_type")
router.register("project-type", views.ProjectTypeViewSet, basename="project_type")
router.register("purpose-plan", views.PurposePlanViewSet, basename="purpose_plan")
router.register(
    "project-process", views.ProjectProcessViewSet, basename="project_process"
)
router.register(
    "project-nature", views.ProjectNatureViewSet, basename="project_process"
)
router.register("project-level", views.ProjectLevelViewSet, basename="project_level")
router.register(
    "project-proposed-type",
    views.ProjectProposedTypeViewSet,
    basename="project_proposed_type",
)
router.register(
    "project-activity", views.ProjectActivityViewSet, basename="project_activity"
)
router.register("purchase-type", views.PurchaseTypeViewSet, basename="purchase_type")
router.register("priority-type", views.PriorityTypeViewSet, basename="priority_type")
router.register(
    "selection-feasibility",
    views.SelectionFeasibilityViewSet,
    basename="selection_feasibility",
)
router.register("strategic-sign", views.StrategicSignViewSet, basename="strategic_sign")
router.register("program", views.ProgramViewSet, basename="program")
router.register(
    "target-group-category",
    views.TargetGroupCategoryViewSet,
    basename="target_group_category",
)
router.register("target-group", views.TargetGroupViewSet, basename="target_group")
router.register("project-status", views.ProjectStatusViewSet, basename="project_status")
router.register("contract-type", views.ContractTypeViewSet, basename="contract_type")
router.register("office", views.OfficeViewSet, basename="office")
router.register(
    "standing-list-type", views.StandingListTypeViewSet, basename="standing_list_type"
)
router.register("standing-list", views.StandingListViewSet, basename="standing_list")
router.register("road-type", views.RoadTypeViewSet, basename="road_type")
router.register("road-status", views.RoadStatusViewSet, basename="road_status")
router.register("drainage_type", views.DrainageTypeViewSet, basename="drainage-type")
router.register("road", views.RoadViewSet, basename="road")
router.register("currency", views.CurrencyViewSet, basename="currency")
router.register("module", views.ModuleViewSet, basename="module")
router.register("sub-module", views.SubModuleViewSet, basename="sub_module")
router.register("news-paper", views.NewsPaperViewSet, basename="news_paper")
router.register(
    "project-start-decision",
    views.ProjectStartDecisionViewSet,
    basename="project_start_decision",
)
router.register(
    "construction-material-description",
    views.ConstructionMaterialDescriptionViewSet,
    basename="construction_material_description",
)
router.register(
    "budget-sub-title", views.BudgetSubTitleViewSet, basename="budget_sub_title"
)
router.register("payment-method", views.PaymentMethodViewSet, basename="payment_method")
router.register("source-receipt", views.SourceReceiptViewSet, basename="source-receipt")
router.register(
    "collect-payment", views.CollectPaymentViewSet, basename="collect_payment"
)
router.register("sub-ledger", views.SubLedgerViewSet, basename="sub-ledger")
router.register("atm", views.ATMViewSet, basename="atm")
router.register("budget-source", views.BudgetSourceViewSet, basename="budget_source")
router.register("sbe-type", views.SBETypeViewSet, basename="sbe-type")
router.register("sbe", views.SBEViewSet, basename="sbe")
router.register("document-type", views.DocumentTypeViewSet, basename="document_type")

urlpatterns = router.urls
