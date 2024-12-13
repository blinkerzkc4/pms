from django.apps import apps
from django.contrib import admin

from .models import (
    District,
    DistrictRateFiles,
    Estimate,
    EstimationRate,
    FinancialYear,
    JDComment,
    JobDescription,
    JobDescriptionFile,
    Municipality,
    Project,
    ProjectCategory,
    Province,
    Quantity,
    Rate,
    RateArea,
    RateCategory,
    RateSource,
    Topic,
    Unit,
    Ward,
)


@admin.register(
    District,
    FinancialYear,
    Municipality,
    Province,
    RateCategory,
    RateArea,
    RateSource,
    Topic,
    Ward,
    DistrictRateFiles,
    ProjectCategory,
    Project,
    JobDescription,
    JDComment,
    JobDescriptionFile,
    Estimate,
    EstimationRate,
    Unit,
)
class UserAddAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by",)

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.created_by = request.user
            super().save_model(request, obj, form, change)

        else:
            super().save_model(request, obj, form, change)


@admin.register(Rate)
class RateAdmin(UserAddAdmin):
    list_display = (
        "id",
        "title",
        "title_eng",
        "financial_year",
        "category",
        "topic",
        "source",
        "area",
        "amount",
        "unit",
    )
    list_filter = (
        "financial_year",
        "category",
        "topic",
        "source",
        "area",
        "amount",
        "unit",
    )
    search_fields = (
        "title",
        "title_eng",
    )


@admin.register(
    Quantity,
)
class QuantityAdmin(UserAddAdmin):
    list_display = (
        "id",
        "__str__",
        "s_no",
        "project",
    )
    list_filter = (
        "project",
        "unit",
        "created_by",
    )
    search_fields = ("s_no",)
