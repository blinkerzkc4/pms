import datetime

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from project.models import Project


class PDFExporter:
    def get_context(self, request, data):
        return {
            "data": data,
            "project": Project.objects.filter(
                id=request.GET.get("project")
            ).first(),
            "company_name": request.user.assigned_municipality.office_name,
            "company_sub_name": request.user.assigned_municipality.sub_name,
            "company_address": request.user.assigned_municipality.office_address,
            "email": request.user.assigned_municipality.email,
            "phone": request.user.assigned_municipality.phone,
        }

    def export(self, request, data, **kwargs):
        return self.render_to_pdf(request, data, **kwargs)

    def render_to_pdf(self, request, data, **kwargs):
        context = self.get_context(request, data)

        response = HttpResponse(content_type="application/pdf")
        name = kwargs.get("name", self.name)
        response["Content-Disposition"] = (
            f"inline; attachment; filename={name}-{str(datetime.datetime.now())}.pdf"
        )
        response["Content-Transfer-Encoding"] = "binary"
        html_string = render_to_string(self.template, context=context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())

        result = html.write_pdf()

        response.write(result)

        return response


class QuantityPDFExporter(PDFExporter):
    template = "project/quantity.html"
    name = "quantity"


class EstimationRatePDFExporter(PDFExporter):
    template = "project/estimation_rate.html"
    name = "district-rate"


class TransportationRatePDFExporter(PDFExporter):
    template = "project/transportation_rate.html"
    name = "transportation_rate"


class TOCPDFExporter(PDFExporter):
    template = "project/toc.html"
    name = "toc"


class NormPDFExporter(PDFExporter):
    template = "project/norm.html"
    name = "norm"


class ResourcePDFExporter(PDFExporter):
    template = "project/resource.html"
    name = "resource"


class TratePDFExporter(PDFExporter):
    template = "project/district_transport.html"
    name = "District Rate + Transport"


class SORPDFExporter(PDFExporter):
    template = "project/sor.html"
    name = "Summary of Rates"


class AbstractOfCostPDFExporter(PDFExporter):
    template = "project/abstract_of_cost.html"
    name = "Abstract of Cost"


class SAOCPDFExporter(PDFExporter):
    template = "project/saoc.html"
    name = "Summary Abstract of Cost"


class QuantityEstimatePDFExporter(PDFExporter):
    template = "project/quantity_estimate.html"
    name = "Quantity Estimate Sheet"


class CostEstimatePDFExporter(PDFExporter):
    template = "project/malepa_format/cost_estimate.html"
    name = "Cost Estimate Sheet"
