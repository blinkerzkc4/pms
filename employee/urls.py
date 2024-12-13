"""
-- Created by Bikash Saud
--
-- Created on 2023-06-07
"""
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register("marital-status", views.MaritalStatusViewSet, basename="marital_status")
router.register("department", views.DepartmentViewSet, basename="department")
router.register(
    "department-branch", views.DepartmentBranchViewSet, basename="department_branch"
)
router.register("position-level", views.PositionLevelViewSet, basename="position_level")
router.register("position", views.PositionViewSet, basename="position")
router.register("employee-type", views.EmployeeTypeViewSet, basename="employee_type")
router.register("service-group", views.ServiceGroupViewSet, basename="service_group")
router.register(
    "employee-sector", views.EmployeeSectorViewSet, basename="employee_sector"
)
router.register(
    "current-working-detail",
    views.CurrentWorkingDetailViewSet,
    basename="current_working_detail",
)
router.register("family-detail", views.FamilyDetailViewSet, basename="family_detail")
router.register(
    "enrollment-detail", views.EnrollmentDetailViewSet, basename="enrollment_detail"
)
router.register(
    "cumulative-detail", views.CumulativeDetailViewSet, basename="cumulative_detail"
)
router.register("employee-detail", views.EmployeeViewSet, basename="employee")
router.register("tax-payer", views.TaxPayerViewSet, basename="tax_payer")
router.register("religion", views.ReligionViewSet, basename="religion")
router.register("language", views.LanguageViewSet, basename="language")
router.register("country", views.CountryViewSet, basename="country")
router.register("nationality", views.NationalityViewSet, basename="nationality")
router.register(
    "public-representative-position",
    views.PublicRepresentativePositionViewSet,
    basename="public_representative_position",
)
router.register(
    "public-representative-detail",
    views.PublicRepresentativeDetailViewSet,
    basename="public_representative_detail",
)
urlpatterns = router.urls
