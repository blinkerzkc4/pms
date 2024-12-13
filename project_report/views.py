from django.apps import apps as django_apps
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import datetime_safe
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, validators
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from weasyprint import CSS, HTML

from pratibedan.entities import *
from project_planning.filters import CustomReportTemplateFilter
from project_report.constants.models_for_crt import CRT_MODELS_LIST
from project_report.filters import TemplateFieldMappingFilter
from utils.report_utils import (
    create_crt_field_names,
    get_model_fields,
    get_model_fields_old,
    group_crt_fields,
)

from .models import (
    CustomReportTemplate,
    ReportType,
    TemplateFieldMapping,
    TemplateFieldMappingGroup,
)
from .serializers import (
    CustomReportTemplateSeralizer,
    ReportTypeSeralizer,
    TemplateFieldMappingGroupSerializer,
    TemplateFieldMappingSerializer,
)

# Create your views here.


class TemplateFieldMappingGroupViewSet(ModelViewSet):
    serializer_class = TemplateFieldMappingGroupSerializer
    queryset = TemplateFieldMappingGroup.objects.all()


class TemplateFieldMappingViewSet(ModelViewSet):
    serializer_class = TemplateFieldMappingSerializer
    queryset = TemplateFieldMapping.objects.all()
    filterset_class = TemplateFieldMappingFilter

    def filter_queryset(self, queryset):
        flag = self.request.GET.get("flag", None)
        limit = self.request.GET.get("limit", None)
        pms_process_id = self.request.GET.get("pms_process_id", None)
        status = self.request.GET.get("status", None)
        name = self.request.GET.get("name", None)

        queryset = (
            super()
            .filter_queryset(queryset)
            .filter(~Q(is_deleted=True))
            .order_by("-created_date")
        )
        if flag == "plan_master_only":
            queryset = queryset.filter(Q(pms_process_id=None) & Q(process_name=None))

        elif flag == "app_client_setting":
            queryset = queryset.filter(
                Q(pms_process_id=None) & Q(process_name__icontains="")
            )

        if pms_process_id is not None:
            queryset = queryset.filter(pms_process_id=pms_process_id)

        if status is not None:
            status = bool(status) if type(bool(status)) == bool else True
            queryset = queryset.filter(status=status)
        else:
            queryset = queryset.filter(status=True)

        if name is not None:
            queryset = queryset.filter(
                Q(name__icontains=name) | Q(name_eng__icontains=name)
            )
        return queryset

    def partial_update(self, request, **kwargs):
        instance = get_object_or_404(self.queryset, id=kwargs.get("pk"))

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        instance.updated_by = request.user
        instance.save()
        data = self.serializer_class(instance).data

        return Response(data)

    def update(self, request, **kwargs):
        instance = get_object_or_404(self.queryset, id=kwargs.get("pk"))

        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        instance.updated_by = request.user
        instance.save()
        data = self.serializer_class(instance).data

        return Response(data)

    def destroy(self, request, **kwargs):
        instance = get_object_or_404(self.queryset, id=kwargs.get("pk"))

        instance.deleted_by = request.user
        instance.deleted_on = datetime_safe.datetime.now()
        instance.is_deleted = True
        instance.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request, **kwargs):
        data = request.data
        print(data, 899999999999)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        instance.created_by = request.user
        instance.save()

        seralized_data = self.serializer_class(instance).data

        return Response(seralized_data, status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False)
    def column_names(self, request, *args, **kwargs):
        entities = {
            "municipality_data": MunicipalityData,
            "district_data": DistrictData,
            "province_data": ProvinceData,
            "address_data": AddressData,
            "project_data_response": ProjectDataResponse,
            # "report_by_project_type": ReportByProjectType,
            "project_budget_allocation_data": ProjectBudgetAllocationData,
            "project_agreement_data": ProjectAgreementData,
            "deposit_mandate_data": DepositMandateData,
            "user_committee_data": UserCommitteeData,
            "user_committee_form_data": UserCommitteeFormData,
            "installment_detail_data": InstallmentDetailData,
            "open_contract_account_data": OpenContractAccountData,
            "project_finished_bail_return_data": ProjectFinishedBailReturnData,
            "project_benefited_detail_data": ProjectBenefitedDetailData,
            # "project_report": ProjectReport,
            # "project_report_by_subject_area": ProjectReportBySubjectArea,
            # "project_report_by_agreement": ProjectReportByAgreement,
            # "project_report_by_payment_detail": ProjectReportByPaymentDetail,
        }
        field_names = []
        for variable_name, entity_class in entities.items():
            for field in entity_class.__fields__.keys():
                field_names.append(f"{variable_name}.{field}")
        return Response(field_names)

    @staticmethod
    def get_crt_fields():
        existing_fields = TemplateFieldMapping.objects.all().values_list(
            "code", flat=True
        )
        all_crt_fields = []
        already_included_models = set()
        for crt_model in CRT_MODELS_LIST:
            model = django_apps.get_model(
                app_label=crt_model["app_name"], model_name=crt_model["model"]
            )
            fields, already_included_models = get_model_fields(
                model,
                already_included_models=already_included_models,
                # should_repeat_models=False,
            )
            crt_fields = create_crt_field_names(
                crt_model["crt_field"],
                fields,
                ignore_field_codes=existing_fields,
                initial_crt_model_names=[field["model"] for field in fields],
            )
            all_crt_fields.extend(crt_fields)
        all_crt_fields = group_crt_fields(all_crt_fields)
        return all_crt_fields

    @action(methods=["GET"], detail=False)
    def available_fields(self, request, *args, **kwargs):
        all_crt_fields = self.get_crt_fields()
        return Response(
            all_crt_fields,
            status=status.HTTP_200_OK,
        )

    @action(methods=["PATCH"], detail=True)
    @swagger_auto_schema(
        manual_parameters=[],
        request_body=openapi.Schema(
            "body_schema",
            type=openapi.TYPE_OBJECT,
            properties=None,
        ),
    )
    def restore_template(self, request, pk=None):
        if pk is None:
            raise validators.ValidationError("Invalid url, enter id")

        instance = get_object_or_404(self.queryset, id=pk)

        instance.is_deleted = False
        instance.deleted_by = None
        instance.deleted_on = None
        instance.updated_by = request.user
        instance.save()

        data = self.serializer_class(instance).data
        return Response(data)


class CustomReportTemplateViewSet(ModelViewSet):
    serializer_class = CustomReportTemplateSeralizer
    queryset = CustomReportTemplate.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomReportTemplateFilter

    @action(methods=["POST"], detail=False)
    def print(self, request):
        template_content = request.data.get("template_content", None)

        if template_content is None:
            raise validators.ValidationError("template_content is required")

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"inline; attachment;"
        response["Content-Transfer-Encoding"] = "binary"

        html = HTML(string=template_content, base_url=request.build_absolute_uri())
        css = CSS(string=""" @page{size:A4;margin:0.5in;}""")
        result = html.write_pdf(stylesheets=[css])

        response.write(result)
        return response

    @action(methods=["GET"], detail=True)
    def view(self, request, pk=None):
        instance = get_object_or_404(self.queryset, id=pk)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f"inline; attachment; filename={instance.name}-{instance.template_type_id}.pdf"
        )
        response["Content-Transfer-Encoding"] = "binary"

        html = HTML(
            string=instance.template_content.encode("utf-8").decode("utf-8"),
            base_url=request.build_absolute_uri(),
        )
        css = CSS(string=""" @page{size:A4;margin:0.5in;}""")
        result = html.write_pdf(stylesheets=[css])

        response.write(result)
        return response


class ReportTypeViewSet(ModelViewSet):
    serializer_class = ReportTypeSeralizer
    queryset = ReportType.objects.all()


@api_view(["get"])
def get_report_models(request, *args, **kwargs):
    report_models: dict[str, dict[str, str]] = settings.REPORT_SETTINGS["report_models"]

    report_models_data = []

    for report_model_code, report_model_data in report_models.items():
        report_model = django_apps.get_model(
            report_model_data["app_label"], report_model_data["model"]
        )

        report_models_data.append(
            {"code": report_model_code, "name": report_model._meta.verbose_name.title()}
        )

    return Response(report_models_data)


@api_view(["get"])
def get_report_model_fields(request, report_model_code: str, *args, **kwargs):
    report_models: dict[str, dict[str, str]] = settings.REPORT_SETTINGS["report_models"]

    report_model_data = report_models.get(report_model_code)

    if not report_model_data:
        return Response(
            {
                "message": f"Error! Report Model with code {report_model_code} not found."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    report_model = django_apps.get_model(
        report_model_data["app_label"], report_model_data["model"]
    )

    report_model_fields = []

    for field in report_model._meta.get_fields():
        try:
            field_name = field.verbose_name
        except:
            field_name = field.name
        report_model_fields.append(
            {
                "code": field.name,
                "name": field_name,
                "type": str(type(field)),
            }
        )

    return Response(report_model_fields)
