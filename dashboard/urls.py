from django.urls import path

from dashboard.views import (
    BudgetAnalysis,
    DashboardAPIRootView,
    DashboardOverallProgress,
    DashboardOverview,
    MonitoringAnalysis,
    ProjectDeadlineAnalysis,
    ProjectStatusAnalysis,
    TPPTProjectsAnalysis,
    UPSProjectsAnalysis,
)

app_name = "dashboard"
urlpatterns = [
    path("", DashboardAPIRootView.as_view(), name="root"),
    path("overview/", DashboardOverview.as_view(), name="overview"),
    path(
        "overall-progress/",
        DashboardOverallProgress.as_view(),
        name="overall-progress",
    ),
    path(
        "project-status-analysis/",
        ProjectStatusAnalysis.as_view(),
        name="project-status-analysis",
    ),
    path(
        "budget-analysis/",
        BudgetAnalysis.as_view(),
        name="budget-analysis",
    ),
    path(
        "ups-projects-analysis/",
        UPSProjectsAnalysis.as_view(),
        name="ups-projects-analysis",
    ),
    path(
        "tppt-projects-analysis/",
        TPPTProjectsAnalysis.as_view(),
        name="tppt-projects-analysis",
    ),
    path(
        "monitoring-analysis/",
        MonitoringAnalysis.as_view(),
        name="monitoring-analysis",
    ),
    path(
        "project-deadline-analysis/",
        ProjectDeadlineAnalysis.as_view(),
        name="project-deadline-analysis",
    ),
]
