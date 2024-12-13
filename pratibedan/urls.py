"""
-- Created by Bikash Saud
-- Created on 2023-07-27
"""

from django.urls import path

from . import views

urlpatterns = [
    path(
        "contact-related-investment-report/",
        views.ContractInvestmentReportAPIView.as_view(),
        name="contact_related_investment_report",
    ),
    path(
        "scheme-bid-details/",
        views.SchemeBidReportAPIView.as_view(),
        name="scheme_bid_report",
    ),
    path(
        "not-completed-projects/",
        views.NotCompletedProjectAPIView.as_view(),
        name="not_completed_projects_report",
    ),
    path(
        "project-by-start-process/",
        views.ProjectsByStartProcessAPIView.as_view(),
        name="by_start_process",
    ),
    path(
        "by-project-level/",
        views.ByProjectLevelAPIView.as_view(),
        name="by_project_level",
    ),
    path(
        "by-project-type/",
        views.ByProjectTypeAPIView.as_view(),
        name="by_project_type",
    ),
    path(
        "by-project-subject-area/",
        views.ByProjectSubjectArea.as_view(),
        name="by_project_subject_area",
    ),
    path(
        "by-agreement/",
        views.ByAgreementAPIView.as_view(),
        name="by_agreement",
    ),
    path(
        "by-payment-detail/",
        views.ByPaymentDetailAPIView.as_view(),
        name="by_payment_detail",
    ),
    path(
        "by-physical-progress/",
        views.ByPhysicalProgressAPIView.as_view(),
        name="by_physical_progress",
    ),
    path(
        "address-line/",
        views.AddressLineAPIView.as_view(),
        name="address-line",
    ),
    path(
        "municipality-address/",
        views.MunicipalityAddressAPIView.as_view(),
        name="municipality-address",
    ),
]
