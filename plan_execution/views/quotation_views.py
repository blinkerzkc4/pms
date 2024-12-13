# Quotatton ViewSets
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django_weasyprint.utils import django_url_fetcher
from rest_framework.decorators import action
from weasyprint import CSS, HTML

from base_model.viewsets import (
    ChildCreationSupportViewSet,
    MultipleObjectSupportViewSet,
    MunicipalityAndProjectFilteredViewSet,
)
from plan_execution.models import (
    QuotationFirmDetails,
    QuotationInvitationForProposal,
    QuotationSpecification,
    QuotationSubmissionApproval,
)
from plan_execution.serializers import (
    QuotationFirmDetailsSerializer,
    QuotationInvitationForProposalSerializer,
    QuotationSpecificationSerializer,
    QuotationSubmissionApprovalSerializer,
    SubmissionApprovalFirmDetailsSerializer,
    SubmissionApprovalFirmDetailsUpdateSerializer,
)


class QuotationFirmDetailsViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = QuotationFirmDetailsSerializer
    model = QuotationFirmDetails
    project_execution_field_name = "quot_specification__project"


class QuotationSpecificationViewSet(ChildCreationSupportViewSet):
    serializer_class = QuotationSpecificationSerializer
    model = QuotationSpecification
    project_required = True
    child_payload_properties = [
        {
            "model": QuotationFirmDetails,
            "serializer_class": QuotationFirmDetailsSerializer,
            "child_name": "specification_firm_details",
            "parent_name": "quot_specification",
            "key_in_payload": "firm_details",
        }
    ]
    return_only_one = True
    is_project_process = True
    block_multiple_object_creation = True

    @action(detail=True, methods=["get"])
    def export_ced(self, request, pk=None):
        quotation_specification = self.get_object()

        html_string = render_to_string(
            "plan_execution/quotation/cost_estimate_data.html",
            context={
                "quot_spec": quotation_specification,
            },
            request=request,
        )

        response = HttpResponse(content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = f"inline; attachment; filename=cost-estimate-data-{str(datetime.datetime.now())}.pdf"
        response["Content-Trasnfer-Encoding"] = "binary"

        html = HTML(string=html_string, base_url="/", url_fetcher=django_url_fetcher)
        css = CSS(
            string="@page{size:A4 " + ("landscape") + ";margin:0.44in 0in 0in 0in;}"
        )
        result = html.write_pdf(stylesheets=[css])
        response.write(result)
        return response

    @action(detail=True, methods=["get"])
    def ced_html(self, request, pk=None):
        quotation_specification = self.get_object()

        return render(
            request,
            "plan_execution/quotation/cost_estimate_data.html",
            context={
                "quot_spec": quotation_specification,
            },
        )


class QuotationInvitationForProposalViewSet(MultipleObjectSupportViewSet):
    serializer_class = QuotationInvitationForProposalSerializer
    model = QuotationInvitationForProposal
    project_required = True


class QuotationSubmissionApprovalViewSet(MunicipalityAndProjectFilteredViewSet):
    serializer_class = QuotationSubmissionApprovalSerializer
    model = QuotationSubmissionApproval
    project_required = True


class QuotationSubmissionApprovalFirmDetailsViewSet(
    MunicipalityAndProjectFilteredViewSet
):
    serializer_class = SubmissionApprovalFirmDetailsSerializer
    serializer_mapping = {
        "PUT": SubmissionApprovalFirmDetailsUpdateSerializer,
        "PATCH": SubmissionApprovalFirmDetailsUpdateSerializer,
    }
    model = QuotationFirmDetails
    project_execution_field_name = "quot_specification__project"

    def get_serializer_class(self):
        return self.serializer_mapping.get(self.request.method, self.serializer_class)
