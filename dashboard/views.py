import datetime

from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from plan_execution.models import ProjectExecution
from project.models import FinancialYear
from project.serializers import FinancialYearSerializer
from utils.constants import PROJECT_STATUSES


class DashboardAPIView(APIView):
    def get_projects_list(self, request):
        financial_year = request.query_params.get(
            "financial_year", FinancialYear.current_fy().id
        )
        if financial_year == "all":
            return ProjectExecution.objects.all()
        return ProjectExecution.objects.filter(financial_year__id=financial_year)


class DashboardAPIRootView(APIView):
    def get(self, request: HttpRequest, *args, **kwargs):
        urls = {
            "overview": request.build_absolute_uri(reverse("dashboard:overview")),
            "overall_progress": request.build_absolute_uri(
                reverse("dashboard:overall-progress")
            ),
            "project_status_analysis": request.build_absolute_uri(
                reverse("dashboard:project-status-analysis")
            ),
            "budget_analysis": request.build_absolute_uri(
                reverse("dashboard:budget-analysis")
            ),
            "ups_projects_analysis": request.build_absolute_uri(
                reverse("dashboard:ups-projects-analysis")
            ),
            "tppt_projects_analysis": request.build_absolute_uri(
                reverse("dashboard:tppt-projects-analysis")
            ),
            "monitoring_analysis": request.build_absolute_uri(
                reverse("dashboard:monitoring-analysis")
            ),
            "project_deadline_analysis": request.build_absolute_uri(
                reverse("dashboard:project-deadline-analysis")
            ),
        }
        return Response(urls, status=status.HTTP_200_OK)


# Create your views here.
class DashboardOverview(DashboardAPIView):
    def get(self, request, *args, **kwargs):
        projects = self.get_projects_list(request)
        total = projects.count()

        return Response({"total_amount": 0, "total": total}, status=status.HTTP_200_OK)


class DashboardOverallProgress(DashboardAPIView):
    def get(self, request, *args, **kwargs):
        projects = self.get_projects_list(request)
        total = projects.count()
        completed = len([project for project in projects if project.is_completed])
        delayed = len([project for project in projects if project.is_delayed])
        ongoing = len([project for project in projects if project.is_ongoing])

        return Response(
            {
                "total": total,
                "completed": completed,
                "delayed": delayed,
                "ongoing": ongoing,
            },
            status=status.HTTP_200_OK,
        )


class ProjectStatusAnalysis(DashboardAPIView):
    def get(self, request, *args, **kwargs):
        projects = self.get_projects_list(request)
        project_status_count = {}
        for project in projects:
            project_status_count[project.project_status] = (
                project_status_count.get(project.project_status, 0) + 1
            )
        for project_status in PROJECT_STATUSES:
            project_status_count[project_status] = project_status_count.get(
                project_status, 0
            )
        return Response(project_status_count, status=status.HTTP_200_OK)


class BudgetAnalysis(DashboardAPIView):
    def get(self, request, *args, **kwargs):
        projects = ProjectExecution.objects.all()
        last_financial_years = FinancialYear.last_3_fys()
        budget_analysis_list = []
        for financial_year in last_financial_years:
            fy_budget_analysis = {}
            fy_budget_analysis["fy"] = FinancialYearSerializer(financial_year).data
            project_in_fy = projects.filter(financial_year=financial_year)
            all_paymentexitbills = []
            for project in project_in_fy:
                all_paymentexitbills += project.paymentexitbill_set.all()
            total_budget = sum(
                [
                    payment_exit_bill.nikasha_total_amount or 0
                    for payment_exit_bill in all_paymentexitbills
                ]
            )
            fy_budget_analysis["budget"] = {
                "total_nikasha": total_budget or 0,
            }
            budget_analysis_list.append(fy_budget_analysis)
        return Response(budget_analysis_list, status=status.HTTP_200_OK)


class UPSProjectsAnalysis(DashboardAPIView):
    def get_projects_list(self, request):
        projects = super().get_projects_list(request)
        return projects.filter(start_pms_process__code="ups")

    def get(self, request, *args, **kwargs):
        projects = self.get_projects_list(request)
        agreement_process_completed = len(
            [
                project
                for project in projects
                if project.openingcontractaccount_set.exists()
                and project.openingcontractaccount_set.first().is_agreement_done
            ]
        )
        budget_allocated = len(
            [
                project
                for project in projects
                if project.project_budget_allocation_detail.exists()
            ]
        )
        first_notice_published = len(
            [
                project
                for project in projects
                if project.project_consumer_formulation.exists()
                and project.project_consumer_formulation.first().first_time_publish
            ]
        )
        first_installment_paid = len(
            [
                project
                for project in projects
                if project.paymentexitbill_set.filter(
                    installment__code="first"
                ).exists()
            ]
        )
        return Response(
            {
                "total": len(projects),
                "agreement_process_completed": agreement_process_completed,
                "budget_allocated": budget_allocated,
                "first_notice_published": first_notice_published,
                "first_installment_paid": first_installment_paid,
            },
            status=status.HTTP_200_OK,
        )


class TPPTProjectsAnalysis(DashboardAPIView):
    def get_projects_list(self, request):
        projects = super().get_projects_list(request)
        return projects.filter(start_pms_process__code="tppt")

    def get(self, request, *args, **kwargs):
        projects = self.get_projects_list(request)
        agreement_process_completed = len(
            [
                project
                for project in projects
                if project.projectagreement_set.exists()
                and project.projectagreement_set.first().is_agreement_done
            ]
        )
        budget_allocated = len(
            [
                project
                for project in projects
                if project.project_budget_allocation_detail.exists()
            ]
        )
        first_notice_published = len(
            [
                project
                for project in projects
                if project.project_tender.exists()
                and project.project_tender.first().first_published_date is not None
            ]
        )
        first_installment_paid = len(
            [
                project
                for project in projects
                if project.paymentexitbill_set.filter(
                    installment__code="first"
                ).exists()
            ]
        )
        return Response(
            {
                "total": len(projects),
                "agreement_process_completed": agreement_process_completed,
                "budget_allocated": budget_allocated,
                "first_notice_published": first_notice_published,
                "first_installment_paid": first_installment_paid,
            },
            status=status.HTTP_200_OK,
        )


class MonitoringAnalysis(DashboardAPIView):
    def get_projects_list(self, request):
        projects = super().get_projects_list(request)
        return projects.filter(start_pms_process__code="ups")

    def get(self, request, *args, **kwargs):
        projects = self.get_projects_list(request)
        monitorings = [
            project.usercommitteemonitoring_set.first()
            for project in projects
            if project.usercommitteemonitoring_set.exists()
        ]

        return Response(
            {
                "total": len(monitorings),
                "completed": len(
                    [monitoring for monitoring in monitorings if monitoring.is_done]
                ),
                "ongoing": len(
                    [
                        monitoring
                        for monitoring in monitorings
                        if monitoring.is_done is False
                    ]
                ),
            },
            status=status.HTTP_200_OK,
        )


class ProjectDeadlineAnalysis(DashboardAPIView):
    def get(self, request, *args, **kwargs):
        projects = self.get_projects_list(request)
        projects = [
            project for project in projects if project.deadline_date is not None
        ]
        today_date = datetime.date.today()
        one_week_later_date = today_date + datetime.timedelta(days=7)
        fifteen_days_later_date = today_date + datetime.timedelta(days=15)
        one_month_later_date = today_date + datetime.timedelta(days=30)
        two_month_later_date = today_date + datetime.timedelta(days=60)

        project_deadlines = {
            "total": len(projects),
            "deadlines": {
                "today": {
                    "expired": len(
                        [
                            project
                            for project in projects
                            if project.deadline_date == today_date
                        ]
                    ),
                    "ongoing": len(
                        [
                            project
                            for project in projects
                            if project.deadline_date > today_date
                        ]
                    ),
                },
                "one_week_later": {
                    "expired": len(
                        [
                            project
                            for project in projects
                            if project.deadline_date < one_week_later_date
                        ]
                    ),
                    "ongoing": len(
                        [
                            project
                            for project in projects
                            if project.deadline_date > one_week_later_date
                        ]
                    ),
                },
                "fifteen_days_later": {
                    "expired": len(
                        [
                            project
                            for project in projects
                            if project.deadline_date < fifteen_days_later_date
                        ]
                    ),
                    "ongoing": len(
                        [
                            project
                            for project in projects
                            if project.deadline_date > fifteen_days_later_date
                        ]
                    ),
                },
                "one_month_later": {
                    "expired": len(
                        [
                            project
                            for project in projects
                            if project.deadline_date < one_month_later_date
                        ]
                    ),
                    "ongoing": len(
                        [
                            project
                            for project in projects
                            if project.deadline_date > one_month_later_date
                        ]
                    ),
                },
                "two_month_later": {
                    "expired": len(
                        [
                            project
                            for project in projects
                            if project.deadline_date < two_month_later_date
                        ]
                    ),
                    "ongoing": len(
                        [
                            project
                            for project in projects
                            if project.deadline_date > two_month_later_date
                        ]
                    ),
                },
            },
        }
        return Response(project_deadlines, status=status.HTTP_200_OK)
