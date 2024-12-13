"""
-- Created by Bikash Saud
-- Created on 2023-06-25
"""
import datetime

from django.http import HttpResponse
from django.template.loader import render_to_string
from django_weasyprint.utils import django_url_fetcher
from weasyprint import CSS, HTML


def render_to_pdf(request, template, context, landscape: bool = False):
    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = f"inline; attachment; filename=pms_nepal-{str(datetime.datetime.now())}.pdf"
    response["Content-Trasnfer-Encoding"] = "binary"

    html_string = render_to_string(template, context=context)
    html = HTML(string=html_string, base_url="/", url_fetcher=django_url_fetcher)
    css = CSS(
        string="@page{size:A4 "
        + ("landscape" if landscape else "portrait")
        + ";margin:0.44in 0in 0in 0in;}"
    )
    result = html.write_pdf(stylesheets=[css])
    response.write(result)
    return response
