from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(
    "custom-report-field-mapping-group",
    views.TemplateFieldMappingGroupViewSet,
    basename="template_field_mapping_group",
)
router.register(
    "custom-report-field-mapping",
    views.TemplateFieldMappingViewSet,
    basename="template_field_mapping",
)

router.register(
    "custom-report-template",
    views.CustomReportTemplateViewSet,
    basename="custom_report_template",
)

router.register("report-type", views.ReportTypeViewSet, basename="report_type")

urlpatterns = [
    path("", include(router.urls)),
    path("report_models/", views.get_report_models, name="report_models"),
    path(
        "report_model_fields/<str:report_model_code>/",
        views.get_report_model_fields,
        name="report_model_fields",
    ),
]
