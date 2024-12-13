import datetime

from django.http import HttpRequest
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base_model.export_views.data.export_models import get_export_model
from utils.excel_generate import get_excel_response


class ExcelView(APIView):
    def get(self, request: HttpRequest, *args, **kwargs):
        request_type = self.request.GET.get("request_type")
        if not request_type:
            return Response(
                {"error": "request_type is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        export_model = get_export_model(request_type)

        if not export_model:
            return redirect("base_model:excel-old")

        data, display_fields, title = export_model

        context = {
            "data": data,
            "display_fields": display_fields,
            "title": title,
            "request": request,
            "date": datetime.datetime.now().date(),
            "company_name": request.user.assigned_municipality.office_name,
            "company_sub_name": request.user.assigned_municipality.sub_name,
            "company_address": request.user.assigned_municipality.office_address,
            "email": request.user.assigned_municipality.email,
            "phone": request.user.assigned_municipality.phone,
            "column_widths": [15, 40, 40, 40],
        }

        return get_excel_response(context)
