import logging
from decimal import Decimal

from django.conf import settings
from django.db.models import Q
from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from norm.filters import NormFilter
from norm.models import ActivityType, Norm, NormActivity, NormComponent, NormExtraCost
from norm.serializers import (
    ActivityTypeSerializer,
    NormActivitySerializer,
    NormComponentSerializer,
    NormExportSerializer,
    NormExtraCostSerializer,
    NormSerializer,
)
from project.models import Unit
from utils.excel_import.norms import import_norms_data
from utils.export.excel_export import NormExcelExporter

logger = logging.getLogger("Norms View")
logging.basicConfig(level=logging.INFO)


class ActivityTypeViewSet(ModelViewSet):
    serializer_class = ActivityTypeSerializer

    def get_queryset(self):
        qs = ActivityType.objects.all()
        municipality = self.request.user.assigned_municipality_id
        if municipality:
            qs = qs.filter(municipality=municipality)
        return qs

    def perform_create(self, serializer):
        serializer.save(municipality=self.request.user.assigned_municipality)


class NormActivityViewSet(ModelViewSet):
    serializer_class = NormActivitySerializer
    filterset_fields = ("activity_type",)

    def get_queryset(self):
        qs = NormActivity.objects.all()
        municipality = self.request.user.assigned_municipality_id
        if municipality:
            qs = qs.filter(municipality=municipality)
        return qs

    def perform_create(self, serializer):
        serializer.save(municipality=self.request.user.assigned_municipality)


class NormExtraCostViewSet(ModelViewSet):
    serializer_class = NormExtraCostSerializer

    def get_queryset(self):
        qs = NormExtraCost.objects.all()
        municipality = self.request.user.assigned_municipality_id
        if municipality:
            qs = qs.filter(municipality=municipality)
        return qs

    def perform_create(self, serializer):
        serializer.save(municipality=self.request.user.assigned_municipality)


class NormComponentViewSet(ModelViewSet):
    serializer_class = NormComponentSerializer
    filterset_fields = ("norm__title", "component_type")
    queryset = NormComponent.objects.all().select_related(
        "unit",
        "category",
        "category__category",
        "category__topic",
        "category__topic__parent",
        "category__topic__parent__parent",
        "category__financial_year",
        "norm",
        "norm__project",
    )


class NormViewSet(ModelViewSet):
    serializer_class = NormSerializer
    filterset_fields = (
        "activity__activity_type",
        "activity",
        "project",
        "subpart_description",
        "item_description",
        "specification_no",
        "unit__name",
    )
    filterset_class = NormFilter

    def get_queryset(self):
        qs = Norm.objects.all()
        # municipality = self.request.user.assigned_municipality_id
        # if municipality and not self.request.user.is_superuser:
        #     qs = qs.filter(municipality=municipality)
        qs.select_related(
            "project",
            "unit",
            "normextracost_set",
            "normcomponent_set__category",
            "normcomponent_set__category__topic",
            "normcomponent_set__category__financial_year",
            "normcomponent_set__unit",
            "normcomponent_set__rate",
            "municipality",
        )
        return qs

    @action(detail=False, methods=["post"])
    def add_many(self, request, *args, **kwargs):
        serializer = self.serializer_class(many=True, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(municipality=request.user.assigned_municipality)
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    def deactivate(self, request, *args, **kwargs):
        norm = self.get_object()
        norm.status = False
        norm.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def activate(self, request, *args, **kwargs):
        norm = self.get_object()
        norm.status = True
        norm.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def export(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        if request.GET.get("project", None) is None:
            qs = qs.filter(project=None)

        file_type = request.GET.get("file_type", "excel")
        norms_export_serializer = NormExportSerializer(qs, many=True)
        if file_type == "excel":
            return NormExcelExporter.quick_export(request, norms_export_serializer.data)
        else:
            return Response(
                {"message": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["get", "post"], url_path="import")
    def import_excel(self, request, *args, **kwargs):
        logger.info("Importing norms data")
        logger.info("Request method: %s", request.method)
        if request.method == "GET":
            template_path = (
                settings.BASE_DIR / "templates" / "import" / "Norms Template.xlsx"
            )
            return FileResponse(open(template_path, "rb"), as_attachment=True)
        if request.method == "POST":
            excel_file = request.FILES.get("excel_file")
            activity = request.data.get("activity", None)
            if not excel_file and not activity:
                return Response(
                    {"message": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST
                )
            worksheet_name = request.data.get("worksheet_name", None)

            try:
                norms_data = import_norms_data(excel_file, worksheet_name)
            except Exception as e:
                return Response(
                    {"message": "Error in processing file"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for norm_data_index, norm_data in enumerate(norms_data):
                norm_data["activity"] = activity

                if norm_data.get("unit"):
                    unit = Unit.objects.filter(
                        Q(name_eng=norm_data["unit"])
                        | Q(name_unicode=norm_data["unit"])
                        | Q(name=norm_data["unit"])
                    ).first()
                    if unit is None:
                        unit = Unit.objects.create(
                            name=norm_data["unit"],
                            name_eng=norm_data["unit"],
                            name_unicode=norm_data["unit"],
                        )
                    norm_data["unit"] = unit.id
                else:
                    norm_data["unit"] = None

                for labour_component in norm_data.get("labour_component", []):
                    if labour_component.get("unit"):
                        unit = Unit.objects.filter(
                            Q(name_eng=labour_component["unit"])
                            | Q(name_unicode=labour_component["unit"])
                            | Q(name=labour_component["unit"])
                        ).first()
                        if unit is None:
                            unit = Unit.objects.create(
                                name=labour_component["unit"],
                                name_eng=labour_component["unit"],
                                name_unicode=labour_component["unit"],
                            )
                        labour_component["unit"] = unit.id
                    else:
                        labour_component["unit"] = None

                for material_component in norm_data.get("material_component", []):
                    if material_component.get("unit"):
                        unit = Unit.objects.filter(
                            Q(name_eng=material_component["unit"])
                            | Q(name_unicode=material_component["unit"])
                            | Q(name=material_component["unit"])
                        ).first()
                        if unit is None:
                            unit = Unit.objects.create(
                                name=material_component["unit"],
                                name_eng=material_component["unit"],
                                name_unicode=material_component["unit"],
                            )
                        material_component["unit"] = unit.id
                    else:
                        material_component["unit"] = None

                for equipment_component in norm_data.get("equipment_component", []):
                    if equipment_component.get("unit"):
                        unit = Unit.objects.filter(
                            Q(name_eng=equipment_component["unit"])
                            | Q(name_unicode=equipment_component["unit"])
                            | Q(name=equipment_component["unit"])
                        ).first()
                        if unit is None:
                            unit = Unit.objects.create(
                                name=equipment_component["unit"],
                                name_eng=equipment_component["unit"],
                                name_unicode=equipment_component["unit"],
                            )
                        equipment_component["unit"] = unit.id
                    else:
                        equipment_component["unit"] = None

            serializer = self.serializer_class(data=norms_data, many=True)

            try:
                serializer.is_valid(raise_exception=True)
                serializer.save(municipality=request.user.assigned_municipality)
                return Response(
                    {"success": True, "message": "Norms imported successfully."},
                    status=status.HTTP_200_OK,
                )
            except ValidationError as e:
                return Response(
                    {"success": False, "message": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"message": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())

        if request.GET.get("project", None) is None:
            qs = qs.filter(project=None)

        norms = qs.order_by("item_id", "part_id", "sub_part_id")
        item_map = {}
        part_map = {}
        i = 1
        data = []
        norm_datas = NormSerializer(norms, many=True).data
        for norm, norm_data in zip(norms, norm_datas):
            filtered_norm_components = norm.normcomponent_set.all()
            if request.GET.get("resource_title") or request.GET.get(
                "resource_title_eng"
            ):
                filtered_norm_components = norm.normcomponent_set.filter(
                    Q(category__title__icontains=request.GET.get("resource_title", ""))
                    & Q(
                        category__title_eng__icontains=request.GET.get(
                            "resource_title_eng", ""
                        )
                    )
                )
            if request.GET.get("resource_rate"):
                filtered_norm_components = filtered_norm_components.filter(
                    category__amount=Decimal(request.GET.get("resource_rate"))
                )
            if request.GET.get("resource_unit"):
                filtered_norm_components = filtered_norm_components.filter(
                    unit__name=request.GET.get("resource_unit")
                )

            print(norm.normcomponent_set.all())
            print(filtered_norm_components)

            if not filtered_norm_components.exists():
                continue

            desc = norm.description
            parent = 0
            if norm.subpart_description:
                desc = norm.subpart_description
                if norm.part_id not in item_map:
                    item_map[norm.part_id] = i
                    data.append(
                        {
                            "item_id": norm.item_id,
                            "oid": i,
                            "parent": 0,
                            "description": norm.description,
                            "type": "PART",
                            "is_leaf": False,
                        }
                    )
                    i += 1
                parent = part_map.get(norm.item_id)
            if norm.item_description:
                desc = norm.item_description
                if norm.part_id not in part_map:
                    part_map[norm.part_id] = i
                    data.append(
                        {
                            "part_id": norm.part_id,
                            "oid": i,
                            "parent": parent,
                            "description": norm.subpart_description,
                            "type": "SUBPART",
                            "is_leaf": False,
                        }
                    )
                    i += 1
                parent = part_map.get(norm.part_id)

            # norm_data = NormSerializer(norm).data
            norm_data.update(
                {
                    "oid": i,
                    "parent": parent,
                    "type": "ITEM",
                    "description": desc,
                    "is_leaf": True,
                }
            )
            data.append(norm_data)
        return Response(data, status=status.HTTP_200_OK)
