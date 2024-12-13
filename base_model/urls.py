"""
-- Created by Bikash Saud
--
-- Created on 2023-06-07
"""
from django.urls import path
from rest_framework import routers

from base_model.export_views.excel import ExcelView

from . import views

router = routers.DefaultRouter()

router.register("gender", views.GenderViewSet, basename="gender")
router.register("address", views.AddressViewSet, basename="address")
urlpatterns = router.urls

app_name = "base_model"
urlpatterns += [
    path("pdf/", views.PdfView.as_view(), name="pdf"),
    path("excel/", ExcelView.as_view(), name="excel"),
    path("excel_old/", views.ExcelViewOld.as_view(), name="excel-old"),
    path("csv/", views.CsvView.as_view(), name="csv"),
]
