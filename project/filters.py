import django_filters

from .models import Estimate, Project


class ProjectFilter(django_filters.FilterSet):
    fiscal_year = django_filters.CharFilter(
        field_name="financial_year__fy", lookup_expr="iexact"
    )
    name = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="iexact"
    )

    class Meta:
        model = Project
        fields = ["fiscal_year", "name"]


class EstimateFilter(django_filters.FilterSet):
    project = django_filters.NumberFilter(field_name="project__id")

    class Meta:
        model = Estimate
        fields = ["project"]
