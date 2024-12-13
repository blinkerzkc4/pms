from django.http import HttpResponse
from django_weasyprint.utils import django_url_fetcher
from weasyprint import CSS, HTML


def get_pdf_response(content, filename):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; attachment; filename="{filename}.pdf"'
    response["Content-Transfer-Encoding"] = "binary"

    pdf_html = HTML(string=content, base_url="/", url_fetcher=django_url_fetcher)
    pdf_css = CSS(string="@page{size:A4;margin:0.5in;}")

    pdf = pdf_html.write_pdf(stylesheets=[pdf_css])

    response.write(pdf)
    return response
