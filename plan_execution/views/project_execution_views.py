import datetime

from django.db.models import Q
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app_settings.entities import Setting
from plan_execution.filters import ProjectExecutionFilter
from plan_execution.models import (
    CommentAndOrder,
    ConsumerFormulation,
    DepositMandate,
    EstimationSubmitAcceptance,
    InstitutionalCollaborationMandate,
    InstitutionalCollaborationNominatedStaff,
    MeasuringBook,
    OpeningContractAccount,
    PaymentExitBill,
    ProbabilityStudyApprove,
    ProjectAgreement,
    ProjectBidCollection,
    ProjectDarbhauBid,
    ProjectDeadline,
    ProjectExecution,
    ProjectFinishedBailReturn,
    ProjectMobilization,
    ProjectModifiedReport,
    ProjectRevision,
    ProjectTender,
    QuotationInvitationForProposal,
    QuotationSpecification,
    QuotationSubmissionApproval,
    UserCommitteeMonitoring,
    UserCommitteeProjectWorkComplete,
)
from plan_execution.serializers import ProjectExecutionSerializer
from project.models import FinancialYear, Project
from project_report.choices import FieldTypeChoices
from project_report.models import CustomReportTemplate, ReportType, TemplateFieldMapping
from utils.constants import (
    TEMPLATE_ENDING_BLOCK,
    TEMPLATE_LOAD_TAGS,
    TEMPLATE_STARTING_BLOCK,
)
from utils.export.pdf_export import get_pdf_response
from utils.nepali_date import ad_to_bs
from utils.render_template_from_string import template_from_string
from utils.report.template_processor import (
    extract_variables_from_template,
    get_main_variable_names_from_template,
)


class ProjectExecutionViewSet(ModelViewSet):
    serializer_class = ProjectExecutionSerializer
    queryset = ProjectExecution.objects.all().order_by("created_date")
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectExecutionFilter

    def filter_queryset(self, queryset):
        filter_query = Q()

        if self.request.user.assigned_municipality:
            filter_query &= Q(
                project__municipality=self.request.user.assigned_municipality
            )
        if self.request.user.assigned_ward:
            filter_query &= Q(project__ward=self.request.user.assigned_ward)
        # else:
        #     filter_query &= Q(project__ward__isnull=True)

        return super().filter_queryset(queryset).filter(filter_query)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        try:
            project = Project.objects.create(
                financial_year=FinancialYear.current_fy(),
                municipality=request.user.assigned_municipality,
            )
            instance.project = project
            instance.save()

        except Exception as e:
            print(e)

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @property
    def report_models(self):
        return {
            "consumer_formulation": ConsumerFormulation,
            "probability_study_approve": ProbabilityStudyApprove,
            "opening_contract_account": OpeningContractAccount,
            "user_committee_monitoring": UserCommitteeMonitoring,
            "project_revision": ProjectRevision,
            "project_mobilization": ProjectMobilization,
            "measuring_book": MeasuringBook,
            "project_deadline": ProjectDeadline,
            "comment_and_order": CommentAndOrder,
            "payment_exit_bill": PaymentExitBill,
            "user_committee_project_work_complete": UserCommitteeProjectWorkComplete,
            "estimation_submit_acceptance": EstimationSubmitAcceptance,
            "project_tender": ProjectTender,
            "project_bid_collection": ProjectBidCollection,
            "project_darbhau_bid": ProjectDarbhauBid,
            "project_agreement": ProjectAgreement,
            "project_finished_bail_return": ProjectFinishedBailReturn,
            "deposit_mandate": DepositMandate,
            "institutional_collaboration_nominated_staff": InstitutionalCollaborationNominatedStaff,
            "institutional_collaboration_mandate": InstitutionalCollaborationMandate,
            # Quotation
            "quot_specification": QuotationSpecification,
            "quot_ifp": QuotationInvitationForProposal,
            "quot_sa": QuotationSubmissionApproval,
        }

    def get_report_data(
        self,
        project_execution_pk,
        request,
        template_text: str = None,
    ):
        report_type_code = request.query_params.get("report_type_code")
        project_execution = ProjectExecution.objects.get(id=project_execution_pk)

        # default report data
        default_report_data = {
            "project_execution": project_execution,
            "current_user": request.user,
            "settings": Setting.open_setting(
                request.user.assigned_municipality, request
            ),
        }

        # extra report data to be extracted from one of the default report data
        # parent is the key of the default report data
        # value is the field name in the parent object
        extra_report_data = {
            "consumer_committee": {
                "parent": "project_execution",
                "value": "selected_consumer_committee",
            },
        }

        # initialising report data with default report data
        report_data = {**default_report_data}

        # getting all the main variable names from the template
        report_variable_names = get_main_variable_names_from_template(template_text)

        for report_variable_name in report_variable_names:
            # getting the report model from the report models
            report_model = self.report_models.get(report_variable_name)
            report_object = None
            if report_model is None:
                if report_variable_name not in extra_report_data:
                    continue

                # Getting the parent object and the field name from the extra report data
                extra_report_model_parent, extra_report_model_field_name = (
                    extra_report_data[report_variable_name]["parent"],
                    extra_report_data[report_variable_name]["value"],
                )

                # Getting the report object from the parent object and the field name
                report_object = getattr(
                    default_report_data[extra_report_model_parent],
                    extra_report_model_field_name,
                )
            elif (
                report_variable_name == "payment_exit_bill"
                and report_type_code.startswith("nikasha_report_btn_")
            ):
                # Getting the index of the installment from the report type code
                try:
                    installment_code_index = int(report_type_code.split("_")[-1]) - 1
                except:
                    installment_code_index = 0

                installment_codes_list = [
                    "first",
                    "second",
                    "third",
                    "fourth",
                    "last",
                ]

                report_object = report_model.objects.filter(
                    project=project_execution,
                    installment__code=installment_codes_list[installment_code_index],
                ).first()
            else:
                report_object = report_model.objects.filter(
                    project=project_execution
                ).first()

            if report_object is None:
                continue

            report_data[report_variable_name] = report_object

        non_db_columns_crt_fields = TemplateFieldMapping.objects.filter(
            ~Q(field_type=FieldTypeChoices.DB_COLUMN),
        )

        extra_non_db_columns_data = {
            non_db_columns_crt_field.code_only: non_db_columns_crt_field.report_code_for_template
            for non_db_columns_crt_field in non_db_columns_crt_fields
        }

        return {
            **report_data,
            **extra_non_db_columns_data,
            "today_date": ad_to_bs(),
        }

    def get_crt(self, request: Request):
        report_type_code = request.query_params.get("report_type_code")
        pms_process_id = request.query_params.get("pms_process_id")

        custom_report_template = CustomReportTemplate.objects.filter(
            (
                Q(template_type_id__code=report_type_code)
                & Q(client_id=request.user)
                & Q(start_pms_process__id=pms_process_id)
            )
            | (
                Q(template_type_id__code=report_type_code)
                & Q(is_template_default=True)
                & Q(start_pms_process__id=pms_process_id)
            )
            | (Q(template_type_id__code=report_type_code) & Q(is_template_default=True))
        )

        # custom_report_template = CustomReportTemplate.objects.filter(
        #     template_type_id__code=report_type_code,
        #     client_id=request.user,
        #     start_pms_process__id=pms_process_id,
        # )

        # if not custom_report_template.exists():
        #     custom_report_template = CustomReportTemplate.objects.filter(
        #         template_type_id__code=report_type_code,
        #         is_template_default=True,
        #         start_pms_process__id=pms_process_id,
        #     )

        # if not custom_report_template.exists():
        #     custom_report_template = CustomReportTemplate.objects.filter(
        #         template_type_id__code=report_type_code,
        #         is_template_default=True,
        #     )

        if not custom_report_template.exists():
            try:
                custom_report_id = int(report_type_code)
            except:
                custom_report_id = None
            if custom_report_id:
                custom_report_template = CustomReportTemplate.objects.filter(
                    id=custom_report_id,
                )

        return custom_report_template

    def get_report_header(self, crt: CustomReportTemplate):
        header_html = ""
        if crt.is_report_header_show:
            template_type_id_code = (
                "ward_letter_head" if crt.is_ward_template else "main_letter_head"
            )
            letter_head_crt = CustomReportTemplate.objects.filter(
                template_type_id__code=template_type_id_code
            ).first()
            if letter_head_crt:
                header_html = letter_head_crt.template_content.encode("utf-8").decode(
                    "utf-8"
                )
        return header_html

    def get_template_from_crt(
        self, crt: CustomReportTemplate, load_header: bool = True
    ):
        header_html = self.get_report_header(crt)

        if not crt.template_content:
            raise ValueError("Template content is empty.")

        variables = extract_variables_from_template(
            crt.template_content.encode("utf-8").decode("utf-8")
        )

        template_html = crt.template_content.encode("utf-8").decode("utf-8")

        for variable in variables:
            if len(variable) < 2:
                continue
            template_html = template_html.replace(
                "{{" + variable + "}}", "{{" + variable + '|default_if_none:""}}'
            )

        template_string = (
            TEMPLATE_STARTING_BLOCK
            + (header_html if load_header else "")
            + template_html
            + TEMPLATE_ENDING_BLOCK
        )

        return template_from_string(template_string)

    def render_template(self, template, context, request, required_renders=1):
        render_count = 0
        template_content = ""
        while render_count <= required_renders:
            template_content = template.render(context=context, request=request)
            if render_count != required_renders:
                template_content = TEMPLATE_LOAD_TAGS + template_content
            template = template_from_string(template_content)
            render_count += 1
        return template_content

    @action(detail=True, methods=["get"])
    def report_html(self, request, pk, *args, **kwargs):
        custom_report_template = self.get_crt(request).first()

        if not custom_report_template:
            return Response(
                {
                    "success": False,
                    "message": f"Template not found. Code: {request.query_params.get('report_type_code')}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        template = self.get_template_from_crt(custom_report_template)
        report_data = self.get_report_data(
            pk,
            request,
            custom_report_template.template_content.encode("utf-8").decode("utf-8"),
        )

        template_content = self.render_template(
            template,
            report_data,
            request,
            required_renders=custom_report_template.required_renders,
        )

        return HttpResponse(template_content)

    @action(detail=True, methods=["get"], url_name="generate_project_report")
    def report(self, request, pk, *args, **kwargs):
        try:
            # Getting report related information from the query params
            report_type_code = request.query_params.get("report_type_code")
            pms_operation_process_id = request.query_params.get("pms_process_id")
            clear_m_report = bool(request.query_params.get("clear_m_report", 0))

            custom_report_template = self.get_crt(request).first()

            if not custom_report_template:
                return Response(
                    {
                        "success": False,
                        "message": f"Template not found. Code: {report_type_code}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            modified_project_report = ProjectModifiedReport.objects.filter(
                project__id=pk,
                report_type__code=report_type_code,
                start_pms_process__id=pms_operation_process_id,
            )

            template_content = ""

            if modified_project_report.exists() and not clear_m_report:
                template_html = modified_project_report.first().report_content

                header_html = self.get_report_header(custom_report_template)

                if header_html:
                    template_content = template_content.replace(
                        "<body>", f"<body>{header_html}"
                    )

                template_string = (
                    TEMPLATE_STARTING_BLOCK
                    + header_html
                    + template_html
                    + TEMPLATE_ENDING_BLOCK
                )
                template = template_from_string(template_string)
                template_content = template.render(
                    context={
                        "current_user": request.user,
                        "settings": Setting.open_setting(
                            request.user.assigned_municipality, request
                        ),
                    },
                    request=request,
                )
            else:
                modified_project_report.delete()
                template = self.get_template_from_crt(custom_report_template)
                report_data = self.get_report_data(
                    pk,
                    request,
                    custom_report_template.template_content.encode("utf-8").decode(
                        "utf-8"
                    ),
                )

                template_content = self.render_template(
                    template,
                    report_data,
                    request,
                    required_renders=custom_report_template.required_renders,
                )

            return get_pdf_response(
                template_content,
                f"{custom_report_template.template_type_id.code}-{str(datetime.datetime.now())}",
            )
        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get", "post"], url_name="modify_project_report")
    def m_report(self, request, pk, *args, **kwargs):
        # Getting report related information from the query params
        report_type_code = request.query_params.get("report_type_code")
        pms_operation_process_id = request.query_params.get("pms_process_id")
        clear_modified_report = bool(request.query_params.get("clear_m_report", 0))

        # Getting the template according to the request data.
        custom_report_template = self.get_crt(request).first()

        # Error if the requested template is not found.
        if not custom_report_template:
            return Response(
                {
                    "success": False,
                    "message": f"Template not found. Code: {report_type_code}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        (
            modified_project_report,
            modified_report_created,
        ) = ProjectModifiedReport.objects.get_or_create(
            project__id=pk,
            report_type__code=report_type_code,
            start_pms_process__id=pms_operation_process_id,
        )

        if not modified_report_created and clear_modified_report:
            modified_project_report.delete()
            modified_project_report = ProjectModifiedReport.objects.create(
                project_id=pk,
                report_type=ReportType.objects.get(code=report_type_code),
                start_pms_process_id=pms_operation_process_id,
            )

        if request.method == "POST":
            template_content_data = request.data.get("template_content")

            if template_content_data and not modified_report_created:
                modified_project_report.report_content = template_content_data
                modified_project_report.save()

            template_content = modified_project_report.report_content
        else:
            if modified_project_report.report_content:
                template_content = modified_project_report.report_content
            else:
                template = self.get_template_from_crt(
                    custom_report_template, load_header=False
                )
                report_data = self.get_report_data(
                    pk,
                    request,
                    custom_report_template.template_content.encode("utf-8").decode(
                        "utf-8"
                    ),
                )

                template_content = self.render_template(
                    template,
                    report_data,
                    request,
                    required_renders=custom_report_template.required_renders,
                )
                modified_project_report.report_content = template_content
                modified_project_report.save()

        return Response(
            {
                "success": True,
                "data": template_content,
                "template_content": template_content,
            },
            status=status.HTTP_200_OK,
        )
