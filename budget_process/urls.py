"""
-- Created by Bikash Saud
--
-- Created on 2023-06-17
"""

from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(
    "expense-budget-range-determine",
    views.ExpenseBudgetRangeDetermineViewSet,
    basename="expense_budget_range_determine",
)

router.register(
    "income-budget-range-determine",
    views.IncomeBudgetRangeDetermineViewSet,
    basename="income_budget_range_determine",
)
router.register("efa", views.EFAViewSet, basename="efa")
router.register(
    "budget-expense-management",
    views.BudgetExpenseManagementViewSet,
    basename="budget_expense_management",
)
router.register(
    "budget-transfer", views.BudgetTransferViewSet, basename="budget_transfer"
)

router.register(
    "budget-ammend", views.BudgetAmmendmentViewSet, basename="budget_ammend"
)

router.register(
    "budget-management", views.BudgetManagementViewSet, basename="budget_management"
)

urlpatterns = router.urls
urlpatterns += [
    path(
        "expense-determine-level/",
        views.ExpenseDetermineLevelViewSet.as_view(),
        name="expense_determine_level",
    ),
]
