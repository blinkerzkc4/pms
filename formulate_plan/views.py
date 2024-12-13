from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from formulate_plan.models import (
    ProjectDocument,
    ProjectWorkType,
    WorkClass,
    WorkProject,
)
from formulate_plan.serializers import (
    ProjectDocumentSerializer,
    ProjectWorkTypeSerializer,
    WorkClassSerializer,
    WorkProjectSerializer,
)
from project_planning.filters import (
    ProjectDocumentFilter,
    ProjectWorkTypeFilter,
    WorkProjectFilter,
)


class WorkClassViewSet(ModelViewSet):
    serializer_class = WorkClassSerializer
    queryset = WorkClass.objects.all()


class ProjectWorkTypeViewSet(ModelViewSet):
    serializer_class = ProjectWorkTypeSerializer
    queryset = ProjectWorkType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectWorkTypeFilter


class WorkProjectViewSet(ModelViewSet):
    serializer_class = WorkProjectSerializer
    queryset = WorkProject.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkProjectFilter

    def list(self, request, *args, **kwargs):
        try:
            project_status = self.request.query_params.get("project_status")
            if project_status == "prioritized":
                queryset = WorkProject.objects.filter(
                    is_approved=False, is_prioritized=True
                )
            elif project_status == "approved":
                queryset = WorkProject.objects.filter(
                    is_approved=True, is_prioritized=True
                )
            elif project_status:
                queryset = WorkProject.objects.filter(
                    project_level__id=project_status,
                    is_approved=False,
                    is_prioritized=False,
                )
            else:
                queryset = WorkProject.objects.all()

            serializer = WorkProjectSerializer(queryset, many=True)
            response_data = {
                "count": len(serializer.data),
                "next": None,
                "previous": None,
                "results": serializer.data,
            }
            return Response(response_data)
        except Exception as e:
            print(f"Exception: {e}")
            return Response(
                {
                    "success": False,
                    "message": "Please ensure that the parameters provided are valid and meet the requirements.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class WorkProjectDocumentViewSet(ModelViewSet):
    serializer_class = ProjectDocumentSerializer
    queryset = ProjectDocument.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectDocumentFilter

    # def filter_queryset(self, queryset):
    #     report_codes = self.request.query_params.get("report_codes[]", [])
    #     if report_codes and isinstance(report_codes, str):
    #         report_codes = [report_codes]
    #     if report_codes:
    #         queryset = queryset.filter(report_type__code__in=report_codes)

    #     return super().filter_queryset(queryset)
