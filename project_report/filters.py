import django_filters

from project_report.models import TemplateFieldMapping


class TemplateFieldMappingFilter(django_filters.FilterSet):
    execution_process = django_filters.CharFilter(
        field_name="pms_process_id__id", lookup_expr="exact"
    )
    group = django_filters.CharFilter(field_name="group__id", lookup_expr="exact")

    class Meta:
        model = TemplateFieldMapping
        fields = {
            "code": ["exact"],
            "name": ["icontains"],
            "status": ["exact"],
        }
