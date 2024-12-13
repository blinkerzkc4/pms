from decimal import Decimal

from django.db.models import Q
from django_filters import rest_framework as filters

from norm.models import Norm


class NormFilter(filters.FilterSet):
    unit = filters.CharFilter(field_name="unit__name", method="filter_unit")
    activity_type = filters.CharFilter(
        field_name="activity__activity_type", lookup_expr="icontains"
    )
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    title_eng = filters.CharFilter(field_name="title_eng", lookup_expr="icontains")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    description_eng = filters.CharFilter(
        field_name="description_eng", lookup_expr="icontains"
    )

    def filter_title(self, queryset, name, value):
        titles_q_model = Q()
        if value:
            titles = value.split("?")
            titles_q_model = Q(title__icontains=titles[0])
            for t in titles[1:]:
                titles_q_model |= Q(title__icontains=t)
        return queryset.filter(titles_q_model)

    def filter_title_eng(self, queryset, name, value):
        titles_q_model = Q()
        if value:
            titles = value.split("?")
            titles_q_model = Q(title_eng__icontains=titles[0])
            for t in titles[1:]:
                titles_q_model |= Q(title_eng__icontains=t)
        return queryset.filter(titles_q_model)

    def filter_unit(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(unit__name__icontains=value) | Q(unit__name_eng__icontains=value)
            )
        return queryset

    class Meta:
        model = Norm
        fields = {
            "activity_no": ["exact"],
            "activity": ["exact"],
            "project": ["exact"],
            "subpart_description": ["exact"],
            "item_description": ["exact"],
            "specification_no": ["exact"],
        }
