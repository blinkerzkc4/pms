from collections import defaultdict
from decimal import Decimal
from itertools import chain

from django.conf import settings
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from openpyxl import load_workbook
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from norm.models import Norm, NormComponent
from project.export.excel_export import *
from project.export.pdf_export import (
    AbstractOfCostPDFExporter,
    CostEstimatePDFExporter,
    EstimationRatePDFExporter,
    NormPDFExporter,
    QuantityEstimatePDFExporter,
    QuantityPDFExporter,
    ResourcePDFExporter,
    SAOCPDFExporter,
    SORPDFExporter,
    TOCPDFExporter,
    TransportationRatePDFExporter,
    TratePDFExporter,
)
from project.filters import EstimateFilter, ProjectFilter
from project.import_estimate import QuantityExtractor
from project.models import (
    District,
    Estimate,
    EstimationRate,
    FederalType,
    FinancialYear,
    JDComment,
    JobDescription,
    JobDescriptionFile,
    Municipality,
    Project,
    ProjectCategory,
    Province,
    Quantity,
    Rate,
    RateArea,
    RateCategory,
    RateSource,
    SummaryExtra,
    Topic,
    Unit,
    Ward,
)
from project.serializers import (
    AreaSerializer,
    DistrictRateCreateSerializer,
    DistrictRateSerializer,
    DistrictRateViewSerializer,
    DistrictSerializer,
    EstimateSerializer,
    EstimationRateSerializer,
    FederalAddressProvinceSerializer,
    FederalTypeSerializer,
    FinancialYearSerializer,
    JDCommentSerializer,
    JobDescriptionFileSerializer,
    JobDescriptionSerializer,
    MunicipalitySerializer,
    ProjectCategorySerializer,
    ProjectCopySerializer,
    ProjectSerializer,
    ProvinceSerializer,
    QuantityImportCreateSerializer,
    QuantitySerializer,
    RateCategorySerializer,
    RateSerializer,
    RateSourceSerializer,
    SummaryExtraSerializer,
    TopicSerializer,
    UnitSerializer,
    WardSerializer,
)
from project_planning.filters import FinancialYearFilter, UnitFilter
from user.permissions import ActiveUserPermission
from utils.excel_import.district_rate import import_district_rate_data
from utils.excel_import.quantity_estimate import (
    import_old_template,
    import_quantity_estimate,
)


def copy_norm(norm, project):
    components = list(norm.normcomponent_set.all())
    costs = list(norm.normextracost_set.all())

    current_id = norm.pk
    norm.pk = None
    norm._state.adding = True
    norm.project_id = project
    if not norm.created_from:
        norm.created_from_id = current_id
    norm.save()
    for c in chain(components, costs):
        c.pk = None
        c._state.adding = True
        c.norm = norm
        c.save()
    return norm


class WardViewSet(ModelViewSet):
    serializer_class = WardSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Ward.objects.none()
        if user.is_superuser:
            return Ward.objects.all()
        return Ward.objects.filter(municipality=user.assigned_municipality)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MunicipalityViewSet(ModelViewSet):
    serializer_class = MunicipalitySerializer
    permission_classes = [ActiveUserPermission]

    def get_queryset(self):
        return Municipality.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FederalTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = FederalTypeSerializer
    queryset = FederalType.objects.all()


class ProvinceViewSet(ReadOnlyModelViewSet):
    serializer_class = ProvinceSerializer

    def get_queryset(self):
        return Province.objects.all()


class DistrictViewSet(ReadOnlyModelViewSet):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        return District.objects.all()


class JobDescriptionViewSet(ModelViewSet):
    serializer_class = JobDescriptionSerializer

    def get_queryset(self):
        return JobDescription.objects.all()


class JDCommentViewSet(ModelViewSet):
    serializer_class = JDCommentSerializer

    def get_queryset(self):
        return JDComment.objects.all()


class UnitViewSet(ModelViewSet):
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UnitFilter


class SourceViewSet(ModelViewSet):
    serializer_class = RateSourceSerializer
    queryset = RateSource.objects.all()


class AreaViewSet(ModelViewSet):
    serializer_class = AreaSerializer
    queryset = RateArea.objects.all()


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filterset_class = ProjectFilter

    @action(detail=False, methods=["post"], serializer_class=ProjectCopySerializer)
    def copy(self, request):
        """
        from_project:<int> Project id of the project to copy (older project)
        to_project:<int> Project id of project to which estimate is to be added from current project

        both the parameters are required
        """
        current_project = request.data.get("from_project")
        target_project = request.data.get("to_project")
        if not (target_project and current_project):
            return Response(
                {
                    "success": False,
                    "message": "Current project and target project are required parameters",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_project = Project.objects.get(id=current_project)
        current_estimate = current_project.estimate
        if not current_estimate:
            return Response(
                {
                    "success": False,
                    "message": "Current project does not have estimate to copy",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            current_estimate.pk = None
            current_estimate._state.adding = True
            current_estimate.project_id = target_project
            current_estimate.save()
        except Exception as e:
            pass

        quantities = Quantity.objects.filter(project=current_project)
        rates = EstimationRate.objects.filter(project=current_project)
        norms = Norm.objects.filter(project=current_project)
        try:
            id_map = {}
            for val in chain(quantities, rates, norms):
                if isinstance(val, Norm):
                    copy_norm(val, target_project)
                    continue
                prev_id = val.id
                val.pk = None
                val._state.adding = True
                val.project_id = target_project
                if hasattr(val, "parent") and val.parent:
                    val.parent_id = id_map.get(val.parent_id, None)
                val.save()
                id_map[prev_id] = val.id
        except:
            print(e)

        return Response(
            {"success": True, "message": "project copied"}, status=status.HTTP_200_OK
        )


class TopicViewSet(ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


class EstimationRateViewSet(ModelViewSet):
    serializer_class = EstimationRateSerializer
    filterset_fields = ("rate__category", "part_name", "project")

    def get_queryset(self):
        return EstimationRate.objects.all().select_related(
            "rate",
            "rate__topic",
            "rate__topic__parent",
            "rate__topic__parent__parent",
            "unit",
        )

    def lists(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        data = EstimationRateSerializer(qs, many=True).data
        added_tps_stps = set()
        new_data = []
        for d in data:
            row_data = d.pop("rate_value", {})
            row_data["rate_id"] = row_data["id"]
            row_data.update(d)
            level = row_data["level"]
            row_type = "ITEM" if level != 1 else "TOPIC"
            row_data.update({"row_type": row_type})
            row_data["isDisabled"] = False

            if level == 1:
                new_data.append(row_data)
                continue

            topic_id = row_data.get("topic_id", 0)
            sub_topic_id = row_data.get("subtopic_id", 0)

            if topic_id not in added_tps_stps:
                to_add = dict(
                    topic_id=topic_id,
                    sub_topic_id=sub_topic_id,
                    item_id=0,
                    sub_topic=row_data.get("sub_topic", ""),
                    sub_topic_unicode=row_data.get("sub_topic_unicode", ""),
                    part_name=row_data.get("part_name", ""),
                    isDisabled=True,
                    row_type="TOPIC",
                )
                new_data.append(to_add)
                added_tps_stps.add(topic_id)
            if sub_topic_id not in added_tps_stps:
                to_add = dict(
                    topic_id=topic_id,
                    sub_topic_id=sub_topic_id,
                    sub_topic=row_data.get("sub_topic", ""),
                    sub_topic_unicode=row_data.get("sub_topic_unicode", ""),
                    part_name=row_data.get("part_name", ""),
                    item_id=0,
                    isDisabled=True,
                    row_type="",
                )
                new_data.append(to_add)
                added_tps_stps.add(sub_topic_id)

            new_data.append(row_data)

        new_data = sorted(
            new_data,
            key=lambda x: (
                x.get("topic_id") or 0,
                x.get("sub_topic_id") or 0,
                x.get("item_id") or 0,
            ),
        )

        id_map = {}
        for i, d in enumerate(new_data):
            d["oid"] = i
            topic = d["topic_id"]
            sub_topic = d["sub_topic_id"]
            row_type = d["row_type"]
            if row_type == "TOPIC":
                parent = 0
                id_map[topic] = i
            elif row_type == "SUB_TOPIC":
                parent = id_map.get(topic)
                id_map[sub_topic] = i
            elif row_type == "ITEM":
                parent = id_map.get(sub_topic or topic)
            d["parent"] = parent

        return Response(new_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def add_many(self, request):
        serializer = self.serializer_class(many=True, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            rates = []
            for data in serializer.data:
                data.pop("unit_value", None)
                data.pop("rate_value", None)
                data["project_id"] = data.pop("project", None)
                data["unit_id"] = data.pop("unit", None)
                data["rate_id"] = data.pop("rate", None)
                rates.append(EstimationRate(**data))
            EstimationRate.objects.bulk_create(rates)
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class EstimateViewSet(ModelViewSet):
    serializer_class = EstimateSerializer
    queryset = Estimate.objects.all()
    filterset_class = EstimateFilter

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     logged_in_user = self.request.user
    #     if logged_in_user.is_superuser:
    #         return queryset

    #     if logged_in_user.assigned_municipality and logged_in_user.assigned_ward:
    #         return queryset.filter(
    #             project__municipality=self.request.user.assigned_municipality,
    #             project__ward=self.request.user.assigned_ward,
    #         )

    #     if logged_in_user.assigned_municipality:
    #         return queryset.filter(
    #             project__municipality=logged_in_user.assigned_municipality
    #         )

    def filter_queryset(self, queryset):
        filtered_queryset = super().filter_queryset(queryset)
        if not filtered_queryset.exists():
            project_id = self.request.GET.get("project")
            project = Project.objects.filter(id=project_id).first()
            if project:
                Estimate.objects.create(
                    project=project,
                    title=project.name or f"Project {project.id} Estimate",
                )
                filtered_queryset = super().filter_queryset(queryset)
        return filtered_queryset

    def create(self, request, *args, **kwargs):
        project_id = request.data.get("project")
        if self.get_queryset().filter(project=project_id).exists():
            return Response(
                self.get_serializer(
                    self.get_queryset().filter(project=project_id).first()
                ).data,
                status=status.HTTP_201_CREATED,
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.file:
            wb = load_workbook(instance.file.path, data_only=True)

            qex = QuantityExtractor(wb, project=instance.project)
            qex.import_data()

    @staticmethod
    def get_summary_of_rates(project):
        quantities = Quantity.objects.filter(project=project).order_by(
            "partid", "parent_id"
        )

        parts = {}
        topics = {}
        norm_map = {}
        topic_quantities = defaultdict(Decimal)
        for quantity in quantities:
            if quantity.norm:
                norm_map[quantity.norm_id] = quantity.norm
            qtype = quantity.type
            if qtype == "PART":
                parts[quantity.id] = quantity
                if not quantity.children:
                    topics[(quantity.norm_id, quantity.id, quantity.parent_id)] = (
                        quantity
                    )
                    if quantity.quantity:
                        topic_quantities[quantity.id] = quantity.quantity
            elif qtype == "SUB_PART" and not quantity.children.exists():
                topics[(quantity.norm_id, quantity.id, quantity.parent_id)] = quantity
                topic_quantities[quantity.id] = quantity.quantity
            elif qtype == "TOPIC":
                topics[(quantity.norm_id, quantity.id, quantity.parent_id)] = quantity
                if quantity.quantity:
                    topic_quantities[quantity.id] = quantity.quantity
            elif qtype == "SUB_TOPIC" and not quantity.children.exists():
                topic_quantities[quantity.parent_id] += quantity.quantity or 0
            elif qtype == "ITEM":
                topic_quantities[quantity.parent.parent_id] += quantity.quantity or 0
        output = []
        added = set()
        from norm.serializers import NormSerializer

        for counter, dict_data in enumerate(topics.items(), start=1):
            k, v = dict_data
            n, qid, pid = k
            n = norm_map.get(n, None)
            if pid not in added:
                q = parts.get(pid, None)
                if q:
                    data = {
                        "pid": pid,
                        "description": q.description,
                        "type": "TOPIC",
                        "provisional": q.provisional,
                        "remarks": q.remarks,
                    }
                    if n:
                        norm = {
                            "specification_no": n.specification_no,
                            "activity_no": n.activity_no,
                            "unit": str(n.unit.name_eng) if n.unit else "",
                            "unit_unicode": str(n.unit.name_unicode) if n.unit else "",
                            "amount": NormSerializer(n).data.get("total_amount")
                            / n.unit_value,
                        }
                        data.update(norm)
                    output.append(data)
                    added.add(pid)
            quantity = topic_quantities.get(qid, v.quantity)
            norm = {}
            if n:
                norm = {
                    "specification_no": n.specification_no,
                    "activity_no": n.activity_no,
                    "unit": str(n.unit.name_eng) if n.unit else "",
                    "unit_unicode": str(n.unit.name_unicode) if n.unit else "",
                    "amount": NormSerializer(n).data.get("total_amount") / n.unit_value,
                }

            data = {
                "type": "LINE",
                "pid": pid,
                "quantity": quantity,
                "description": v.description,
                "s_no_counter": counter,
            }
            data.update(norm)
            output.append(data)
        return output

    @action(detail=False, methods=["post", "delete"])
    def delete_all(self, request):
        project = request.GET.get("project")
        if not project:
            return Response(
                {"success": False, "message": "Project is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Quantity.objects.filter(project_id=project).delete()
        Norm.objects.filter(project_id=project).delete()
        EstimationRate.objects.filter(project_id=project).delete()
        Estimate.objects.filter(project_id=project).delete()
        return Response(
            {"success": True, "data": {"deleted": True}}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"])
    def show_summary_of_rate(self, request):
        project = request.GET.get("project")
        output = self.get_summary_of_rates(project)
        return Response({"success": True, "data": output}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def show_cost_estimate(self, request):
        project = request.GET.get("project")
        output = self.get_cost_estimate(project)
        return Response({"success": True, "data": output}, status=status.HTTP_200_OK)

    @staticmethod
    def get_cost_estimate(project):
        output = {}

        topics = Quantity.objects.filter(project_id=project, type="TOPIC")
        if topics.count() == 0:
            topics = Quantity.objects.filter(project_id=project, type="PART")
        topics_data = []
        total_amount = 0

        for s_no, topic in enumerate(topics, start=1):
            _, length, breadth, height, quantity = topic.total_quantities
            topic_data = {
                "s_no": s_no,
                "specification_no": topic.norm.specification_no,
                "activity_no": topic.norm.activity_no,
                "description": topic.description,
                "unit": (
                    topic.unit.name or topic.unit.name_eng or topic.unit.name_unicode
                    if topic.unit
                    else ""
                ),
                "quantity": quantity,
                "length": length,
                "breadth": breadth,
                "height": height,
                "rate": topic.norm.analysed_rate,
            }
            topic_data["amount"] = float(topic_data["quantity"]) * float(
                topic_data["rate"]
            )
            total_amount += topic_data["amount"]

            topics_data.append(topic_data)

        work_chart_staff_cost_percentage = 20
        other_extra_cost_percentage = 15
        work_chart_staff_cost = total_amount * work_chart_staff_cost_percentage / 100
        other_extra_cost = total_amount * other_extra_cost_percentage / 100
        overhead = 0.15 * total_amount
        subtotal = total_amount + overhead
        vat = 0.13 * subtotal
        contingency = 0.015 * subtotal
        grand_total = subtotal + contingency + vat

        output = {
            "topics": topics_data,
            "total_amount": total_amount,
            "cost_estimate_calculations": {
                "work_chart_staff_cost": {
                    "percentage": work_chart_staff_cost_percentage,
                    "amount": work_chart_staff_cost,
                },
                "other_extra_cost": {
                    "percentage": other_extra_cost_percentage,
                    "amount": other_extra_cost,
                },
            },
            "overhead": overhead,
            "subtotal": subtotal,
            "contingency": contingency,
            "vat": vat,
            "grand_total": grand_total,
        }

        return output

    @staticmethod
    def get_abstract_of_cost(project):
        summary = EstimateViewSet.get_summary_of_rates(project)
        output = []

        part_map = defaultdict(int)
        for o in summary:
            if o.get("type") == "TOPIC":
                output.append(o)
            pid = o["pid"]
            part_map[pid] = Decimal(o.get("amount", 0) or 0) * Decimal(
                o.get("quantity", 0) or 0
            ) + Decimal(part_map.get(pid, 0) or 0)
        for o in output:
            o["amount"] = part_map[o["pid"]]
            o["id"] = o["pid"]

        qs = SummaryExtra.objects.filter(project=project)
        extras = SummaryExtraSerializer(qs, many=True).data
        output.extend(extras)

        return output

    @action(detail=False, methods=["get"])
    def show_abstract_of_cost(self, request):
        project = request.GET.get("project")

        output = self.get_abstract_of_cost(project)
        return Response({"success": True, "data": output}, status=status.HTTP_200_OK)


class FinancialYearViewSet(ModelViewSet):
    serializer_class = FinancialYearSerializer
    queryset = FinancialYear.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FinancialYearFilter


class JobDescriptionFileViewSet(ModelViewSet):
    serializer_class = JobDescriptionFileSerializer
    queryset = JobDescriptionFile.objects.all()


class RateCategoryViewSet(ModelViewSet):
    serializer_class = RateCategorySerializer
    queryset = RateCategory.objects.all()


class RateViewSet(ModelViewSet):
    serializer_class = RateSerializer
    queryset = Rate.objects.all()
    filterset_fields = ("financial_year", "category")

    def get_queryset(self):
        request = self.request
        fy = request.GET.get("financial_year")
        fy = fy if fy else FinancialYear.current_fy().id
        return Rate.objects.filter(financial_year=fy)

    @action(detail=False, methods=["get", "post"])
    def copy(self, request):
        current_fy, prev_fy, _ = FinancialYear.last_3_fys()

        rates = Rate.objects.filter(financial_year=prev_fy)
        for rate in rates:
            if Rate.objects.filter(
                topic=rate.topic,
                financial_year=current_fy,
                district=rate.district,
                municipality=rate.municipality,
            ).exists():
                continue
            rate.pk = None
            rate._state.adding = True
            rate.financial_year = current_fy
            rate.save()
        return Response({"success": True}, status=status.HTTP_200_OK)


class ProjectCategoryViewSet(ModelViewSet):
    serializer_class = ProjectCategorySerializer
    queryset = ProjectCategory.objects.all()


class QuantityViewSet(ModelViewSet):
    serializer_class = QuantitySerializer
    queryset = Quantity.objects.all().select_related("unit", "norm")
    filterset_fields = ("project",)
    ordering_fields = ("id", "s_no", "no")
    ordering = "id"

    def add_norm(self, norm: Norm, project: int):
        n = Norm.objects.filter(created_from=norm, project=project)
        if n.exists():
            return n.first()
        norm = copy_norm(norm, project)
        return norm

    def create_estimation_rates(self, project):
        if not project:
            return
        quantities = Quantity.objects.filter(project=project)
        for quantity in quantities:
            if not quantity.norm or (
                quantity.norm and quantity.norm.project_id == project
            ):
                continue
            norm = self.add_norm(quantity.norm, project)
            quantity.norm = norm
            quantity.save()

        quantities = Quantity.objects.filter(project=project)
        norms = quantities.values_list("norm", flat=True).distinct()
        rates = Rate.objects.filter(normcomponent__norm__in=norms).distinct()
        for rate in rates:
            if not EstimationRate.objects.filter(project=project, rate=rate).exists():
                EstimationRate.objects.create(
                    project_id=project, rate=rate, unit=rate.unit, amount=rate.amount
                )

    @action(detail=False, methods=["post"])
    def add_many(self, request):
        data = request.data
        parents = [d.pop("parent", None) for d in data]
        norms = [d.pop("norm_id", None) for d in data]

        ids = [d.pop("id", None) for d in data]
        serializer = self.serializer_class(many=True, data=data)
        project = request.GET.get("project")
        try:
            serializer.is_valid(raise_exception=True)
            parent_map = {}
            for uid, norm, parent, data in zip(ids, norms, parents, serializer.data):
                data.pop("unit_value", None)
                if isinstance(parent, str):
                    parent = parent_map.get(parent, parent)
                project = data.pop("project", None) or project
                data["project_id"] = project
                data["unit_id"] = data.pop("unit", None)
                data["norm_id"] = norm
                if parent:
                    data["parent_id"] = parent
                q = Quantity.objects.create(**data)
                parent_map[uid] = q.id
            self.create_estimation_rates(project)
            return Response({"success": True}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["get","post"])
    def import_excel(self, request):
        if request.method == "GET":
            template_path = settings.BASE_DIR / "templates" / "import" / "Estimate Import Template.xlsx"
            
            return FileResponse(open(template_path, "rb"), as_attachment=True)
        
        excel_file = request.FILES.get("excel_file")
        project_id = request.data.get("project")

        if excel_file is None:
            return Response(
                {"success": False, "message": "Please select excel file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # project = get_object_or_404(Project, id=project_id)

        try:
            quantity_estimate_data = import_quantity_estimate(excel_file)
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Level of Topic in the Quantity Estimate Excel.
        topic_level_in_quantity_estimate: int = 0

        def process_quantity_estimate_data(
            quantity_data: dict, parent_quantity: Quantity = None
        ):
            nonlocal topic_level_in_quantity_estimate
            quantity = None
            quantity_data_type = quantity_data.pop("type", None)
            if quantity_data_type is not None:
                s_no = quantity_data.pop("s_no", "")
                # Getting the norm
                activity_no = quantity_data.pop("activity_no", None)
                specification_no = quantity_data.pop("specification_no", None)
                norm = Norm.objects.filter(
                    activity_no=activity_no, specification_no=specification_no
                ).first()

                description = quantity_data.pop("description", None)
                no = quantity_data.pop("no", 0)
                try:
                    no = float(no)
                except:
                    no = 0
                # Getting the unit
                unit_string = quantity_data.pop("unit", None)
                unit = Unit.objects.filter(
                    Q(name_eng=unit_string)
                    | Q(name_unicode=unit_string)
                    | Q(name=unit_string)
                ).first()
                description_of_quantity = quantity_data.pop(
                    "description_of_quantity", {}
                )
                if quantity_data_type == "total":
                    total = quantity_data.pop("total", None)
                else:
                    total = description_of_quantity.get("total")
                length = description_of_quantity.get("length")
                breadth = description_of_quantity.get("breadth")
                height = description_of_quantity.get("height")

                has_children = len(quantity_data.items()) > 0
                quantity_estimate_level = 0
                if s_no:
                    quantity_estimate_level = len(s_no.split("."))

                if (
                    quantity_estimate_level == 1
                    and quantity_estimate_level != topic_level_in_quantity_estimate
                ):
                    topic_level_in_quantity_estimate = 0

                QUANTITY_ESTIMATE_TYPES = [
                    "PART",
                    "SUB_PART",
                    "TOPIC",
                    "SUB_TOPIC",
                    "ITEM",
                ]

                if 0 < topic_level_in_quantity_estimate < quantity_estimate_level:
                    QUANTITY_ESTIMATE_TYPES = [
                        "SUB_TOPIC",
                        "ITEM",
                    ]

                if quantity_data_type == "total":
                    quantity_estimate_type = "TOTAL"
                elif norm is not None:
                    quantity_estimate_type = "TOPIC"
                else:
                    quantity_estimate_type = QUANTITY_ESTIMATE_TYPES[
                        quantity_estimate_level - topic_level_in_quantity_estimate - 1
                    ]

                if norm is None and parent_quantity is not None:
                    norm = parent_quantity.norm

                if quantity_estimate_type == "TOPIC":
                    topic_level_in_quantity_estimate = quantity_estimate_level
                    description = norm.description or norm.description_eng

                object_creation_data = {
                    "parent": parent_quantity.pk if parent_quantity else None,
                    "quantity_type": (
                        "DIAMETER" if quantity_data.get("quantity_type") else "DEFAULT"
                    ),
                    "project": project_id,
                    "type": quantity_estimate_type,
                    "norm": norm.pk if norm else None,
                    "s_no": s_no,
                    "description": description,
                    "no": no,
                    "length": length,
                    "breadth": breadth,
                    "height": height,
                    "quantity": total,
                    "unit": unit.pk if unit else None,
                }

                object_creation_serializer = QuantityImportCreateSerializer(
                    data=object_creation_data
                )
                object_creation_serializer.is_valid(raise_exception=True)
                quantity = object_creation_serializer.save()

            if len(quantity_data.items()) > 0:
                children = quantity_data.copy()
                for child_id, child_data in children.items():
                    if isinstance(child_data, dict):
                        process_quantity_estimate_data(child_data, quantity)

        for part_id, part_data in quantity_estimate_data.items():
            process_quantity_estimate_data(part_data)

        self.create_estimation_rates(project_id)
        project = Project.objects.filter(id=project_id).first()
        Estimate.objects.create(
            project=project,
            title=project.name or f"Project {project.id} Estimate",
        )
        return Response(
            {"success": True, "message": "Data imported successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def import_excel_old(self, request):
        excel_file = request.FILES.get("excel_file")
        project_id = request.data.get("project")

        if excel_file is None:
            return Response(
                {"success": False, "message": "Please select excel file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # project = get_object_or_404(Project, id=project_id)

        try:
            quantity_estimate_data = import_old_template(excel_file)
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        def process_quantity_estimate_data(
            quantity_data: dict, parent_quantity: Quantity = None
        ):
            quantity = None
            quantity_data_type = quantity_data.pop("type", None)
            if quantity_data_type is not None:
                s_no = quantity_data.pop("s_no", None)
                # Getting the norm
                activity_no = quantity_data.pop("activity_no", None)
                specification_no = quantity_data.pop("specification_no", None)
                norm = Norm.objects.filter(
                    activity_no=activity_no, specification_no=specification_no
                ).first()
                description = quantity_data.pop("description", None)
                no = quantity_data.pop("no", 0)
                try:
                    no = float(no)
                except:
                    no = 0
                # Getting the unit
                unit_string = quantity_data.pop("unit", None)
                unit = Unit.objects.filter(
                    Q(name_eng=unit_string)
                    | Q(name_unicode=unit_string)
                    | Q(name=unit_string)
                ).first()
                description_of_quantity = quantity_data.pop(
                    "description_of_quantity", {}
                )
                if quantity_data_type == "total":
                    total = quantity_data.pop("total", None)
                else:
                    total = description_of_quantity.get("total")
                length = description_of_quantity.get("length")
                breadth = description_of_quantity.get("breadth")
                height = description_of_quantity.get("height")

                has_children = len(quantity_data.items()) > 0
                quantity_estimate_level = 0
                if s_no:
                    quantity_estimate_level = len(s_no.split("."))

                QUANTITY_ESTIMATE_TYPES = [
                    "PART",
                    "SUB_PART",
                    "TOPIC",
                    "SUB_TOPIC",
                    "ITEM",
                ]

                if quantity_data_type == "total":
                    quantity_estimate_type = "TOTAL"
                else:
                    quantity_estimate_type = QUANTITY_ESTIMATE_TYPES[
                        quantity_estimate_level - 1
                    ]

                object_creation_data = {
                    "parent": parent_quantity.pk if parent_quantity else None,
                    "project": project_id,
                    "type": quantity_estimate_type,
                    "norm": norm.pk if norm else None,
                    "s_no": s_no,
                    "description": description,
                    "no": no,
                    "length": length,
                    "breadth": breadth,
                    "height": height,
                    "quantity": total,
                    "unit": unit.pk if unit else None,
                }

                object_creation_serializer = QuantityImportCreateSerializer(
                    data=object_creation_data
                )
                object_creation_serializer.is_valid(raise_exception=True)
                quantity = object_creation_serializer.save()

            if len(quantity_data.items()) > 0:
                children = quantity_data.copy()
                for child_id, child_data in children.items():
                    process_quantity_estimate_data(child_data, quantity)

        for part_id, part_data in quantity_estimate_data.items():
            process_quantity_estimate_data(part_data)

        self.create_estimation_rates(project_id)
        project = Project.objects.filter(id=project_id).first()
        Estimate.objects.create(
            project=project,
            title=project.name or f"Project {project.id} Estimate",
        )
        return Response(
            {"success": True, "message": "Data imported successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def import_excel_old(self, request):
        excel_file = request.FILES.get("excel_file")
        project_id = request.data.get("project")

        if excel_file is None:
            return Response(
                {"success": False, "message": "Please select excel file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # project = get_object_or_404(Project, id=project_id)

        try:
            quantity_estimate_data = import_old_template(excel_file)
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        def process_quantity_estimate_data(
            quantity_data: dict, parent_quantity: Quantity = None
        ):
            quantity = None
            quantity_data_type = quantity_data.pop("type", None)
            if quantity_data_type is not None:
                s_no = quantity_data.pop("s_no", None)
                # Getting the norm
                activity_no = quantity_data.pop("activity_no", None)
                specification_no = quantity_data.pop("specification_no", None)
                norm = Norm.objects.filter(
                    activity_no=activity_no, specification_no=specification_no
                ).first()
                description = quantity_data.pop("description", None)
                no = quantity_data.pop("no", None)
                try:
                    no = float(no)
                except:
                    no = 0
                # Getting the unit
                unit_string = quantity_data.pop("unit", None)
                unit = Unit.objects.filter(
                    Q(name_eng=unit_string)
                    | Q(name_unicode=unit_string)
                    | Q(name=unit_string)
                ).first()
                description_of_quantity = quantity_data.pop(
                    "description_of_quantity", {}
                )
                if quantity_data_type == "total":
                    total = quantity_data.pop("total", None)
                else:
                    total = description_of_quantity.get("total")
                length = description_of_quantity.get("length")
                breadth = description_of_quantity.get("breadth")
                height = description_of_quantity.get("height")

                has_children = len(quantity_data.items()) > 0
                quantity_estimate_level = 0
                if s_no:
                    quantity_estimate_level = len(s_no.split("."))

                QUANTITY_ESTIMATE_TYPES = [
                    "PART",
                    "SUB_PART",
                    "TOPIC",
                    "SUB_TOPIC",
                    "ITEM",
                ]

                if quantity_data_type == "total":
                    quantity_estimate_type = "TOTAL"
                else:
                    quantity_estimate_type = QUANTITY_ESTIMATE_TYPES[
                        quantity_estimate_level - 1
                    ]

                object_creation_data = {
                    "parent": parent_quantity.pk if parent_quantity else None,
                    "project": project_id,
                    "type": quantity_estimate_type,
                    "norm": norm.pk if norm else None,
                    "s_no": s_no,
                    "description": description,
                    "no": no,
                    "length": length,
                    "breadth": breadth,
                    "height": height,
                    "quantity": total,
                    "unit": unit.pk if unit else None,
                }

                object_creation_serializer = QuantityImportCreateSerializer(
                    data=object_creation_data
                )
                object_creation_serializer.is_valid(raise_exception=True)
                quantity = object_creation_serializer.save()

            if len(quantity_data.items()) > 0:
                children = quantity_data.copy()
                for child_id, child_data in children.items():
                    process_quantity_estimate_data(child_data, quantity)

        for part_id, part_data in quantity_estimate_data.items():
            process_quantity_estimate_data(part_data)

        self.create_estimation_rates(project_id)
        project = Project.objects.filter(id=project_id).first()
        Estimate.objects.create(
            project=project,
            title=project.name or f"Project {project.id} Estimate",
        )
        return Response(
            {"success": True, "message": "Data imported successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def export_excel(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            data = self.serializer_class(queryset, many=True).data
            response = QuantityExcelExporter().export(data)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class DistrictRateViewSet(ModelViewSet):
    serializer_class_map = {
        "GET": DistrictRateViewSerializer,
        "POST": DistrictRateCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class_map.get(
            self.request.method, DistrictRateSerializer
        )

    def get_queryset(self):
        return Rate.objects.all()

    def filter_queryset(self, queryset):
        # municipality = self.request.user.assigned_municipality
        # financial_years = FinancialYear.last_3_fys()
        # filtered_queryset = queryset.filter(
        #     municipality=municipality, financial_year__in=financial_years
        # )
        filtered_queryset = queryset
        return super().filter_queryset(filtered_queryset)

    def list(self, request, *args, **kwargs):
        district_rates = self.filter_queryset(self.get_queryset())
        financial_years = FinancialYear.last_3_fys()

        serializer = self.get_serializer(
            {"rates": district_rates, "financial_years": financial_years}
        )

        return Response(serializer.data)


class DistrictRateView(GenericAPIView):
    """
    send a list of values
    [
    DistrictRateSerialzer1, DistrictRateSerializer2, ...
    ]

    """

    serializer_class = DistrictRateCreateSerializer
    queryset = Rate.objects.all()

    @staticmethod
    def parse_single_serializer(data, user):
        topic = data["topic"]
        topic_unicode = data["topic_unicode"]
        sub_topic = data["sub_topic"]
        sub_topic_unicode = data["sub_topic_unicode"]
        item = data["item"]
        item_unicode = data["item_unicode"]
        topic, _ = Topic.objects.get_or_create(
            name_eng=topic, name_unicode=topic_unicode, parent=None
        )
        if sub_topic or sub_topic_unicode:
            topic, _ = Topic.objects.get_or_create(
                name_eng=sub_topic, name_unicode=sub_topic_unicode, parent=topic
            )
        if item or item_unicode:
            topic, _ = Topic.objects.get_or_create(
                name_eng=item, name_unicode=item_unicode, parent=topic
            )
        # assumption: 1 is current fy, 2 is one before that and 3 is the previous previous
        financial_years = FinancialYear.last_3_fys()

        category = data["category"]
        unit = data["unit"]
        title = data["input"]
        title_unicode = data["input_unicode"]
        unit = data["unit"]
        source = data["source"]
        area = data["rate_area"]
        for i, fy in enumerate(financial_years, 1):
            rate = data.get(f"rate_{i}", None)
            if rate:
                Rate.objects.create(
                    municipality=user.assigned_municipality,
                    district=user.assigned_municipality.district,
                    title_eng=title,
                    title=title_unicode,
                    financial_year=fy,
                    category_id=category,
                    amount=rate,
                    unit_id=unit,
                    source_id=source,
                    area_id=area,
                    topic=topic,
                )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(many=True, data=request.data)
        if serializer.is_valid():
            for data in serializer.data:
                self.parse_single_serializer(data, request.user)
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        municipality = request.user.assigned_municipality
        financial_years = FinancialYear.last_3_fys()
        current_fy = FinancialYear.current_fy()
        base_rate_queryset = Rate.objects.filter(
            municipality=municipality, financial_year__in=financial_years
        ).prefetch_related(
            "unit",
            "financial_year",
            "topic",
            "topic__parent",
            "topic__parent__parent",
            "category",
        )
        if base_rate_queryset.count() < 1:
            base_rate_queryset = Rate.objects.all().prefetch_related(
                "unit",
                "financial_year",
                "topic",
                "topic__parent",
                "topic__parent__parent",
                "category",
            )

        title = request.GET.get("title", "")
        title_eng = request.GET.get("title_eng", "")

        rates = base_rate_queryset.filter(
            Q(unit__name__icontains=request.GET.get("unit", ""))
            | Q(unit__name_eng__icontains=request.GET.get("unit", ""))
        ).prefetch_related(
            "unit",
            "financial_year",
            "topic",
            "topic__parent",
            "topic__parent__parent",
            "category",
        )

        category = request.GET.get("category")
        if category is not None:
            rates = rates.filter(category=category)

        fys = [str(fy) for fy in financial_years]

        if not rates:
            rates = {"financial_years": fys, "rates": []}
            return Response(rates, status=status.HTTP_200_OK)

        values = {}
        for rate in rates:
            val = values.get(rate.topic_id, {})
            val["rate"] = rate
            i = fys.index(rate.financial_year.name) + 1
            if rate.financial_year.name == current_fy.name:
                val["id"] = rate.id
            val[f"rate_{i}"] = rate.amount
            values[rate.topic.id] = val

        if request.GET.get("rate"):
            values = {
                k: v
                for k, v in values.items()
                if v.get("rate_1") == Decimal(request.GET.get("rate"))
                or v.get("rate_2") == Decimal(request.GET.get("rate"))
                or v.get("rate_3") == Decimal(request.GET.get("rate"))
            }

        output = []
        level = {}

        for val in values.values():
            # TODO: maybe can get this from serializer to optimize it
            if not val.get("id"):
                continue
            rate = val.pop("rate")
            val["level"] = rate.level
            val["category"] = rate.category.name_eng if rate.category else ""
            val["category_id"] = rate.category.id if rate.category else None
            val["category_unicode"] = (
                rate.category.name_unicode if rate.category else ""
            )
            val["area_id"] = rate.area_id
            val["area"] = rate.area.name_eng if rate.area else ""
            val["source_id"] = rate.source_id
            val["source"] = rate.source.name_eng if rate.source else ""
            val["unit_id"] = rate.unit_id
            val["unit"] = rate.unit.name_eng if rate.unit else ""
            val["unit_unicode"] = rate.unit.name_unicode if rate.unit else ""
            rate_topic = rate.topic
            topic, subtopic, item, *_ = rate_topic._name_unicode.split("-" * 5) + [
                "",
                "",
                "",
            ]
            val["topic_unicode"] = topic
            val["subtopic_unicode"] = subtopic
            val["item_unicode"] = item

            t, st, itm, *_ = rate_topic._name_eng.split("-" * 5) + ["", "", ""]
            val["topic"] = t
            val["subtopic"] = st
            val["item"] = itm
            tps = f"{topic}-----{t}"
            stps = f"{subtopic}-----{st}"
            try:
                if rate.level == 1:
                    output.append(val)
                elif rate.level == 2:
                    val["subtopic"] = ""
                    val["subtopic_unicode"] = ""
                    val["item"] = subtopic
                    val["item_unicode"] = st
                    tpic = level.get(tps, [])
                    tpic.append(val)
                    level[tps] = tpic
                elif rate.level == 3:
                    level[tps] = level.get(tps, {})
                    st = level[tps].get(stps, [])
                    st.append(val)
                    level[tps][stps] = st
            except Exception as e:
                print(e)

        output = self.create_frontend_format(output, level)
        filters = {
            "title": title,
            "title_eng": title_eng,
        }

        def filter_output_data(data, filters):
            title = (
                data["topic_unicode"]
                if data["input_type"] == "TOPIC"
                else data["item_unicode"]
            )
            title_eng = data["topic"] if data["input_type"] == "TOPIC" else data["item"]

            filter_title_text = filters.get("title", "")
            filter_titles = filter_title_text.split("?")
            filter_title_text_eng = filters.get("title_eng", "")
            filter_titles_eng = filter_title_text_eng.split("?")
            filter_titles_satisfied = []
            filter_titles_eng_satisfied = []
            if filter_title_text:
                filter_titles_satisfied = [
                    filter_title in title for filter_title in filter_titles
                ]

            if filter_title_text_eng:
                filter_titles_eng_satisfied = [
                    filter_title in title_eng for filter_title in filter_titles_eng
                ]
            return any(filter_titles_satisfied) or any(filter_titles_eng_satisfied)

        if title or title_eng:
            output = [data for data in output if filter_output_data(data, filters)]
        rates = {"financial_years": fys, "rates": output}
        return Response(rates, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        rate_id = kwargs.get("district_rate_pk")
        if not rate_id:
            return Response(
                {"success": False, "message": "Rate id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        rate = get_object_or_404(Rate, id=rate_id)
        data = request.data
        # {"type":"topic","description":"skilled","description_unicode":"skilled","area":2,"unit":92,"source":2,"rate_1":1200,"rate_2":0,"rate_3":1200}
        rate_type = data.get("type")
        description = data.get("description")
        description_unicode = data.get("description_unicode")
        area_id = data.get("area")
        category_id = data.get("category")
        unit_id = data.get("unit")
        source_id = data.get("source")
        rate_topic = rate.topic
        if rate_type in ["TOPIC", "SUBTOPIC"]:
            rate_topic.name_eng = description
            rate_topic.name_unicode = description_unicode
            rate_topic.save()
        else:
            rate.description = description
            rate.description_unicode = description_unicode
        rate.save()
        financial_years = FinancialYear.last_3_fys()
        for i, fy in enumerate(financial_years, 1):
            fy_rate = data.get(f"rate_{i}", None)
            Rate.objects.filter(topic=rate_topic, financial_year=fy).update(
                amount=fy_rate,
                area_id=area_id,
                unit_id=unit_id,
                category_id=category_id,
                source_id=source_id,
            )
        return Response({"success": True}, status=status.HTTP_200_OK)

    def single_input(self, **data):
        input_type = data.get("input_type")
        disable = input_type != "ITEM"
        level = data.get("level")
        input_type = "TOPIC" if level == 1 else input_type

        return {
            "oid": data.get("oid"),
            "id": data.get("id"),
            "parent_id": data.get("parent", 0),
            "s_no": data.get("s_no", 0),
            "sort_id": data.get("sort_id"),
            "input_type": input_type,
            # "content_eng": "topic1",
            # "content_unicode": "",
            "category_display": data.get("category_eng", data.get("category", "")),
            "category": data.get("category_id"),
            "rate_1": data.get("rate_1", 0),
            "rate_2": data.get("rate_2", 0),
            "rate_3": data.get("rate_3", 0),
            "unit": data.get("unit", ""),
            "unit_id": data.get("unit_id"),
            "area": data.get("area", ""),
            "area_id": data.get("area_id"),
            "source": data.get("source", ""),
            "source_id": data.get("source_id"),
            "topic": data.get("topic", ""),
            "topic_unicode": data.get("topic_unicode", ""),
            "sub_topic": data.get("subtopic", ""),
            "sub_topic_unicode": data.get("subtopic_unicode", ""),
            "item": data.get("item", ""),
            "item_unicode": data.get("item_unicode", ""),
            "isDisable": disable,
        }

    def delete(self, request, *args, **kwargs):
        rate_id = kwargs.get("district_rate_pk")
        if rate_id is None:
            return Response(
                {"success": False, "message": "Rate id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        district_rate = get_object_or_404(Rate, id=rate_id)
        if district_rate.is_used_in_relation:
            return Response(
                {
                    "success": False,
                    "message": "Rate is used in other relation. Cannot delete",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        district_rate.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def add_data(self, data, level, j, parent=0, sort_id=0):
        output = []
        if isinstance(data, list):
            for d in data:
                output.append(
                    self.single_input(
                        input_type="ITEM",
                        oid=j,
                        parent=parent,
                        sort_id=sort_id,
                        **d,
                    )
                )
                j += 1
        else:
            for k in data:
                eng, nep = k.split("-" * 5)
                input_type = "TOPIC" if level == 1 else "SUBTOPIC"
                dta = (
                    {"topic": eng, "topic_unicode": nep}
                    if level == 1
                    else {
                        "subtopic": eng,
                        "subtopicunicode": nep,
                    }
                )
                output.append(
                    self.single_input(
                        input_type=input_type,
                        oid=j,
                        parent=parent,
                        sort_id=sort_id,
                        **dta,
                    )
                )
                j += 1
                j, out = self.add_data(
                    data[k], level + 1, j, parent=j - 1, sort_id=sort_id
                )
                output.extend(out)
                j += 1
        return j, output

    def create_frontend_format(self, data, levels):
        output = []
        j = 1
        level_index = 0
        for level_index, level in enumerate(levels):
            try:
                j, out = self.add_data(
                    {level: levels[level]}, 1, j, sort_id=level_index
                )
                output.extend(out)
            except Exception as e:
                print(e)
        try:
            j, out = self.add_data(data, 1, j, sort_id=level_index + 1)
        except Exception as e:
            print(e)

        output.extend(out)
        return output


@api_view(["GET", "POST"])
def import_district_rate(request):
    if request.method == "GET":
        template_path = (
            settings.BASE_DIR / "templates" / "import" / "District Rate Template.xlsx"
        )

        return FileResponse(open(template_path, "rb"), as_attachment=True)

    excel_file = request.FILES.get("excel_file")
    if excel_file is None:
        return Response(
            {"success": False, "message": "Please select excel file."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        district_rate_data = import_district_rate_data(excel_file)
    except Exception as e:
        return Response(
            {"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )

    for index, data in enumerate(district_rate_data):
        category = RateCategory.objects.filter(
            Q(name_eng=data["category"]) | Q(name=data["category"])
        ).first()
        if category is None:
            category = RateCategory.objects.create(
                name=data["category"], name_eng=data["category"]
            )
        data["category"] = category.id

        unit = Unit.objects.filter(
            Q(name_eng=data["unit"])
            | Q(name_unicode=data["unit"])
            | Q(name=data["unit"])
        ).first()
        if unit is None:
            unit = Unit.objects.create(
                name=data["unit"], name_eng=data["unit"], name_unicode=data["unit"]
            )
        data["unit"] = unit.id

        source = RateSource.objects.filter(
            Q(name_eng=data["source"])
            | Q(name=data["source"])
            | Q(name_unicode=data["source"])
        ).first()
        if source is None:
            source = RateSource.objects.create(
                name=data["source"],
                name_eng=data["source"],
                name_unicode=data["source"],
            )
        data["source"] = source.id

        area = RateArea.objects.filter(
            Q(name_eng=data["rate_area"])
            | Q(name=data["rate_area"])
            | Q(name_unicode=data["rate_area"])
        ).first()
        if area is None:
            area = RateArea.objects.create(
                name=data["rate_area"],
                name_eng=data["rate_area"],
                name_unicode=data["rate_area"],
            )
        data["rate_area"] = area.id

    serializer = DistrictRateCreateSerializer(data=district_rate_data, many=True)

    if serializer.is_valid():
        for data in serializer.data:
            DistrictRateView.parse_single_serializer(data, request.user)
        return Response(
            {"success": True, "message": "Data imported successfully."},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SummaryExtraViewSet(ModelViewSet):
    serializer_class = SummaryExtraSerializer
    filterset_fields = ("project",)

    queryset = SummaryExtra.objects.all()

    @action(detail=False, methods=["post"])
    def add_many(self, request):
        serializer = self.serializer_class(many=True, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CurrentFiscalYearAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            current_fy = FinancialYear.current_fy()
            current_fy = {
                "id": current_fy.id,
                "start_year": current_fy.start_year,
                "end_year": current_fy.end_year,
                "fy": f"{current_fy.start_year}/{current_fy.end_year}",
            }
            return Response(current_fy, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Exception: {e}")
            return Response(
                {"success": False, "message": "Unable to get current fiscal year"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReportViewSet(ModelViewSet):
    filterset_fields = ("project",)
    queryset = Estimate.objects.all()

    # pdf
    @action(detail=False, methods=["get"])
    def toc_pdf(self, request):
        try:
            project = request.GET.get("project")
            qs = Estimate.objects.filter(project=project).first()
            return TOCPDFExporter().export(request, qs)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def rate_pdf(self, request):
        try:
            queryset = EstimationRate.objects.all()
            queryset = self.filter_queryset(queryset)
            response = EstimationRatePDFExporter().export(request, {"data": queryset})
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def transport_pdf(self, request):
        try:
            queryset = EstimationRate.objects.all()
            queryset = self.filter_queryset(queryset)
            response = TransportationRatePDFExporter().export(
                request, {"data": queryset}
            )
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def trate_pdf(self, request):
        try:
            queryset = EstimationRate.objects.all()
            queryset = self.filter_queryset(queryset)
            response = TratePDFExporter().export(request, {"data": queryset})
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def quantity_pdf(self, request):
        try:
            queryset = Quantity.objects.all()
            queryset = self.filter_queryset(queryset)
            qs = queryset.prefetch_related("unit")
            return QuantityPDFExporter().export(request, qs)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def quantity_estimate_excel(self, request):
        queryset = Quantity.objects.all()
        queryset = self.filter_queryset(queryset)
        qs = queryset.order_by("id").prefetch_related("unit")
        return QuantityEstimateExcelExporter.quick_export(
            request, QuantitySerializer(qs, many=True).data
        )

    @action(detail=False, methods=["get"])
    def quantity_estimate_pdf(self, request):
        queryset = Quantity.objects.all()
        queryset = self.filter_queryset(queryset)
        qs = queryset.order_by("id").prefetch_related("unit")
        return QuantityEstimatePDFExporter().export(request, qs)

    @action(detail=False, methods=["get"])
    def cost_estimate_pdf(self, request):
        data = EstimateViewSet.get_cost_estimate(request.GET.get("project"))
        return CostEstimatePDFExporter().export(request, data)

    @action(detail=False, methods=["get"])
    def cost_estimate_excel(self, request):
        data = EstimateViewSet.get_cost_estimate(request.GET.get("project"))
        return CostEstimateExcelExporter.quick_export(request, data)

    @action(detail=False, methods=["get"])
    def sor_pdf(self, request):
        try:
            summary_of_rates = EstimateViewSet.get_summary_of_rates(
                request.GET.get("project")
            )
            data = []
            summary_of_rate_in_topic = []
            for index, summary_of_rate in enumerate(summary_of_rates, start=1):
                if summary_of_rate.get("type") == "TOPIC":
                    if summary_of_rate_in_topic:
                        data.append(
                            {
                                "type": "SUBTOTAL",
                                "amount": sum(
                                    [x.get("amount") for x in summary_of_rate_in_topic]
                                ),
                            }
                        )
                    summary_of_rate_in_topic = []
                else:
                    summary_of_rate_in_topic.append(summary_of_rate)
                data.append(summary_of_rate)
                if index == len(summary_of_rates):
                    data.append(
                        {
                            "type": "SUBTOTAL",
                            "amount": sum(
                                [x.get("amount") for x in summary_of_rate_in_topic]
                            ),
                        }
                    )

            response = SORPDFExporter().export(request, data)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def aoc_pdf(self, request):
        try:
            summary_of_rates = EstimateViewSet.get_summary_of_rates(
                request.GET.get("project")
            )
            processed_summary_of_rates = []
            summary_of_rate_in_topic = []
            for index, summary_of_rate in enumerate(summary_of_rates, start=1):
                if summary_of_rate.get("type") == "TOPIC":
                    if summary_of_rate_in_topic:
                        processed_summary_of_rates.append(
                            {
                                "type": "SUBTOTAL",
                                "amount": sum(
                                    [x.get("amount") for x in summary_of_rate_in_topic]
                                ),
                            }
                        )
                    summary_of_rate_in_topic = []
                else:
                    summary_of_rate_in_topic.append(summary_of_rate)
                processed_summary_of_rates.append(summary_of_rate)
                if index == len(summary_of_rates):
                    processed_summary_of_rates.append(
                        {
                            "type": "SUBTOTAL",
                            "amount": sum(
                                [x.get("amount") for x in summary_of_rate_in_topic]
                            ),
                        }
                    )

            total = sum(
                [
                    x.get("amount")
                    for x in processed_summary_of_rates
                    if x.get("type") == "SUBTOTAL"
                ]
            )
            data = {
                "processed_summary_of_rates": processed_summary_of_rates,
                "total": total,
            }

            response = AbstractOfCostPDFExporter().export(request, data)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def saoc_pdf(self, request):
        try:
            project = request.GET.get("project")
            soac_data = EstimateViewSet.get_abstract_of_cost(project)
            data = {
                "all_soac_data": soac_data,
            }
            total = sum([x.get("amount") or 0 for x in soac_data])
            provisional_sum = 0
            total_with_ps = total + provisional_sum
            total_vat = total_with_ps * Decimal(0.13)
            grand_total = total_with_ps + total_vat
            data["total"] = total
            data["provisional_sum"] = provisional_sum
            data["total_with_ps"] = total_with_ps
            data["total_vat"] = total_vat
            data["grand_total"] = grand_total
            response = SAOCPDFExporter().export(request, data)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def export_resources_pdf(self, request):
        """
        params:
            project: int id of the project
            component_type: Type of the data to get choices: LABOUR, MATERIAL, EQUIPMENT
        """
        project = request.GET.get("project")
        component_type = request.GET.get("category_type")
        norms = Norm.objects.filter(project_id=project)
        name = "resources"
        norms = norms.values_list("id", flat=True)
        components = NormComponent.objects.filter(norm_id__in=norms)
        if component_type:
            components = components.filter(component_type=component_type.upper())
            name = name + f"_{component_type.lower()}"

        ncs = components.values_list(
            "category",
            "quantity",
            "unit__name_eng",
            "unit__name_unicode",
            "category__title",
        )
        id_map = defaultdict(int)
        quantity_map = defaultdict(float)
        for cat, quantity, unit_eng, unit_unicode, title in ncs:
            quantity_map[cat] = Decimal(quantity_map[cat]) + Decimal(quantity)
            id_map[cat] = (title, unit_eng or unit_unicode or "")

        data = []
        for i in id_map:
            title, unit = id_map[i]
            quantity = quantity_map[i]
            data.append({"title": title, "unit": unit, "quantity": quantity})

        return ResourcePDFExporter().export(request, data=data, name=name)

    @action(detail=False, methods=["get"])
    def norms_pdf(self, request):
        queryset = Norm.objects.all()
        print(queryset)
        queryset = self.filter_queryset(queryset)
        print(queryset)
        response = NormPDFExporter().export(request, queryset)
        return response

        try:
            queryset = Norm.objects.all()
            queryset = self.filter_queryset(queryset)
            response = NormPDFExporter().export(request, queryset)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def norms_html(self, request):
        queryset = Norm.objects.all()
        queryset = self.filter_queryset(queryset)
        context = {
            "data": queryset,
            "company_name": request.user.assigned_municipality.office_name,
            "company_sub_name": request.user.assigned_municipality.sub_name,
            "company_address": request.user.assigned_municipality.office_address,
            "email": request.user.assigned_municipality.email,
            "phone": request.user.assigned_municipality.phone,
        }
        return render(request, "project/norm.html", context)

    @action(detail=False, methods=["get"])
    def show_summary_of_rate(self, request):
        project = request.GET.get("project")
        output = EstimateViewSet.get_summary_of_rates(project)
        return Response({"success": True, "data": output}, status=status.HTTP_200_OK)

    # Excel
    @action(detail=False, methods=["get"])
    def toc_excel(self, request):
        try:
            project = request.GET.get("project")
            qs = Estimate.objects.filter(project=project).first()
            return TOCPDFExporter().export(request, qs)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def rate_excel(self, request):
        try:
            queryset = EstimationRate.objects.all()
            queryset = self.filter_queryset(queryset)
            response = DistrictRateExcelExporter().export(request, queryset)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def transport_excel(self, request):
        try:
            queryset = EstimationRate.objects.all()
            queryset = self.filter_queryset(queryset)
            response = TransportExcelExporter().export(request, queryset)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def trate_excel(self, request):
        try:
            queryset = EstimationRate.objects.all()
            queryset = self.filter_queryset(queryset)
            response = TrateExcelExporter().export(request, queryset)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def quantity_excel(self, request):
        try:
            queryset = Quantity.objects.all()
            queryset = self.filter_queryset(queryset)
            qs = queryset.prefetch_related("unit")
            return QuantityPDFExporter().export(request, qs)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def export_resources_excel(self, request):
        """
        params:
            project: int id of the project
            component_type: Type of the data to get choices: LABOUR, MATERIAL, EQUIPMENT
        """
        project = request.GET.get("project")
        component_type = request.GET.get("category_type")
        norms = Norm.objects.filter(project_id=project)
        name = "resources"
        norms = norms.values_list("id", flat=True)
        components = NormComponent.objects.filter(norm_id__in=norms)
        if component_type:
            components = components.filter(component_type=component_type.upper())
            name = name + f"_{component_type.lower()}"

        ncs = components.values_list(
            "category",
            "quantity",
            "unit__name_eng",
            "unit__name_unicode",
            "category__title",
        )
        id_map = defaultdict(int)
        quantity_map = defaultdict(float)
        for cat, quantity, unit_eng, unit_unicode, title in ncs:
            quantity_map[cat] = Decimal(quantity_map[cat]) + Decimal(quantity)
            id_map[cat] = (title, unit_eng or unit_unicode or "")

        data = []
        for i in id_map:
            title, unit = id_map[i]
            quantity = quantity_map[i]
            data.append({"title": title, "unit": unit, "quantity": quantity})

        return ResourceExcelExporter().export(request, data=data, name=name)

    @action(detail=False, methods=["get"])
    def sor_excel(self, request):
        try:
            summary_of_rates = EstimateViewSet.get_summary_of_rates(
                request.GET.get("project")
            )
            data = []
            summary_of_rate_in_topic = []
            for index, summary_of_rate in enumerate(summary_of_rates, start=1):
                if summary_of_rate.get("type") == "TOPIC":
                    if summary_of_rate_in_topic:
                        data.append(
                            {
                                "type": "SUBTOTAL",
                                "amount": sum(
                                    [x.get("amount") for x in summary_of_rate_in_topic]
                                ),
                            }
                        )
                    summary_of_rate_in_topic = []
                else:
                    summary_of_rate_in_topic.append(summary_of_rate)
                data.append(summary_of_rate)
                if index == len(summary_of_rates):
                    data.append(
                        {
                            "type": "SUBTOTAL",
                            "amount": sum(
                                [x.get("amount") for x in summary_of_rate_in_topic]
                            ),
                        }
                    )

            response = SORExcelExporter.quick_export(request, data)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def aoc_excel(self, request):
        try:
            summary_of_rates = EstimateViewSet.get_summary_of_rates(
                request.GET.get("project")
            )
            processed_summary_of_rates = []
            summary_of_rate_in_topic = []
            for index, summary_of_rate in enumerate(summary_of_rates, start=1):
                if summary_of_rate.get("type") == "TOPIC":
                    if summary_of_rate_in_topic:
                        processed_summary_of_rates.append(
                            {
                                "type": "SUBTOTAL",
                                "amount": sum(
                                    [x.get("amount") for x in summary_of_rate_in_topic]
                                ),
                            }
                        )
                    summary_of_rate_in_topic = []
                else:
                    summary_of_rate_in_topic.append(summary_of_rate)
                processed_summary_of_rates.append(summary_of_rate)
                if index == len(summary_of_rates):
                    processed_summary_of_rates.append(
                        {
                            "type": "SUBTOTAL",
                            "amount": sum(
                                [x.get("amount") for x in summary_of_rate_in_topic]
                            ),
                        }
                    )

            total = sum(
                [
                    x.get("amount")
                    for x in processed_summary_of_rates
                    if x.get("type") == "SUBTOTAL"
                ]
            )
            data = {
                "processed_summary_of_rates": processed_summary_of_rates,
                "total": total,
            }

            response = AbstractOfCostExcelExporter.quick_export(request, data)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def saoc_excel(self, request):
        try:
            project = request.GET.get("project")
            soac_data = EstimateViewSet.get_abstract_of_cost(project)
            data = {
                "all_soac_data": soac_data,
            }
            total = sum([x.get("amount") or 0 for x in soac_data])
            provisional_sum = 0
            total_with_ps = total + provisional_sum
            total_vat = total_with_ps * Decimal(0.13)
            grand_total = total_with_ps + total_vat
            data["total"] = total
            data["provisional_sum"] = provisional_sum
            data["total_with_ps"] = total_with_ps
            data["total_vat"] = total_vat
            data["grand_total"] = grand_total
            response = SAOCExcelExporter.quick_export(request, data)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def norms_excel(self, request):
        try:
            queryset = Norm.objects.all()
            queryset = self.filter_queryset(queryset)
            response = NormPDFExporter().export(request, queryset)
            return response
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([ActiveUserPermission])
def federal_addresses(request):
    provinces = Province.objects.all()
    federal_addresses_serializer = FederalAddressProvinceSerializer(
        provinces, many=True
    )
    return Response(federal_addresses_serializer.data, status=status.HTTP_200_OK)
    return Response(federal_addresses_serializer.data, status=status.HTTP_200_OK)
