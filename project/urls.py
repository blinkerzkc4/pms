from django.urls import path
from rest_framework import routers

from user import views as user_views
from . import views

router = routers.SimpleRouter()

router.register("wards", views.WardViewSet, basename="wards")
router.register("federal_types", views.FederalTypeViewSet, basename="federal-types")
router.register("municipalities", views.MunicipalityViewSet, basename="municipalities")
router.register("provinces", views.ProvinceViewSet, basename="provinces")
router.register("districts", views.DistrictViewSet, basename="districts")
router.register("groups", user_views.GroupViewSet, basename="groups")
router.register("roles", user_views.UserRoleViewSet, basename="roles")
router.register("topics", views.TopicViewSet, basename="topics")
router.register(
    "financial-years", views.FinancialYearViewSet, basename="financial-year"
)
router.register("rates", views.RateViewSet, basename="rates")
router.register(
    "rate-categories", views.RateCategoryViewSet, basename="rate-categories"
)
router.register("units", views.UnitViewSet, basename="units")
router.register("sources", views.SourceViewSet, basename="sources")
router.register("areas", views.AreaViewSet, basename="areas")
router.register("jd", views.JobDescriptionViewSet, basename="job_description")
router.register(
    "jd-files", views.JobDescriptionFileViewSet, basename="job-description-files"
)
router.register("jd-comments", views.JDCommentViewSet, basename="jd-comments")
router.register("projects", views.ProjectViewSet, basename="projects")
router.register(
    "project-categories", views.ProjectCategoryViewSet, basename="project-category"
)
router.register(
    "estimation-rate", views.EstimationRateViewSet, basename="estimation-rate"
)

router.register("estimates", views.EstimateViewSet, basename="estimates")
router.register("reports", views.ReportViewSet, basename="reports")
router.register("quantity", views.QuantityViewSet, basename="quantity")
router.register("summary-extra", views.SummaryExtraViewSet, basename="summary-extra")
urlpatterns = router.urls

urlpatterns += [
    path("district_rate/", views.DistrictRateView.as_view(), name="district-rate-list"),
    path(
        "district_rate/import/", views.import_district_rate, name="district-rate-import"
    ),
    path(
        "district_rate/<int:district_rate_pk>/",
        views.DistrictRateView.as_view(),
        name="delete-district-rate",
    ),
    path(
        "current-fiscal-year/",
        views.CurrentFiscalYearAPIView.as_view(),
        name="current-fiscal-year",
    ),
    path("federal-addresses/", views.federal_addresses, name="federal-addresses"),
]
