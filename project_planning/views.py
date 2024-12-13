from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions
from rest_framework.decorators import action
from rest_framework.response import Response

from base_model.models import DocumentType
from project.models import District
from project.serializers import DistrictSerializer
from project_planning.basic_description_serializers import SubjectAreaSerializer
from project_planning.basic_description_views import *
from project_planning.models import (
    BFI,
    AccountTitleManagement,
    BankAccount,
    BankType,
    BudgetSource,
    BudgetSubTitle,
    ChequeFormat,
    CollectPayment,
    ConstructionMaterialDescription,
    ConsumerCommittee,
    ExecutiveAgency,
    MemberType,
    NewsPaper,
    Organization,
    OrganizationType,
    PaymentMedium,
    PaymentMethod,
    ProjectStartDecision,
    SourceBearerEntity,
    SourceBearerEntityType,
    SourceReceipt,
    SubjectArea,
    SubLedger,
)
from project_planning.serializers import (
    ATMSerializer,
    BankAccountSerializer,
    BankAccountViewSerializer,
    BankTypeSerializer,
    BFISerializer,
    BudgetSourceSerializer,
    BudgetSubTitleSerializer,
    ChequeFormatSerializer,
    CollectPaymentSerializer,
    ConstructionMaterialDescriptionSerializer,
    ConsumerCommitteeDocumentSerializer,
    ConsumerCommitteeMemberSerializer,
    ConsumerCommitteeSerializer,
    CurrencySerializer,
    DocumentTypeSerializer,
    ExecutiveAgencySerializer,
    MemberTypeSerializer,
    ModuleSerializer,
    MonitoringCommitteeDocumentSerializer,
    MonitoringCommitteeMemberSerializer,
    MonitoringCommitteeSerializer,
    NewsPaperSerializer,
    OrganizationSerializer,
    OrganizationTypeSerializer,
    PaymentMediumSerializer,
    PaymentMethodSerializer,
    ProjectStartDecisionSerializer,
    SBESerializer,
    SBETypeSerializer,
    SourceReceiptSerializer,
    SubLedgerSerializer,
    SubModuleSerializer,
)

from .filters import SourceBearerEntityFilter

# Create your views here.


class DistrictViewSet(ModelViewSet):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class SubjectAreaViewSet(ModelViewSet):
    serializer_class = SubjectAreaSerializer
    queryset = SubjectArea.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectAreaFilter

    def list(self, request, *args, **kwargs):
        try:
            parent = self.request.query_params.get("parent")
            display_all = self.request.query_params.get("display_all")
            if parent:
                queryset = SubjectArea.objects.filter(parent__id=parent)
            else:
                if display_all:
                    queryset = SubjectArea.objects.all()
                else:
                    queryset = SubjectArea.objects.filter(parent__isnull=True)
            serializer = SubjectAreaSerializer(queryset, many=True)
            response_data = {
                "count": len(serializer.data),
                "next": None,
                "previous": None,
                "results": serializer.data,
            }
            return Response(response_data)
        except Exception as e:
            raise e


class PaymentMediumViewSet(ModelViewSet):
    serializer_class = PaymentMediumSerializer
    queryset = PaymentMedium.objects.all()


class BankTypeViewSet(ModelViewSet):
    serializer_class = BankTypeSerializer
    queryset = BankType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BankTypeFilter


class ChequeFormatViewSet(ModelViewSet):
    serializer_class = ChequeFormatSerializer
    queryset = ChequeFormat.objects.all()


class BFIViewSet(ModelViewSet):
    serializer_class = BFISerializer
    queryset = BFI.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BFIFilter


class BankAccountViewSet(ModelViewSet):
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BankAccountFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BankAccountViewSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = BankAccountViewSerializer(queryset, many=True)
        response_data = {
            "count": len(serializer.data),
            "next": None,
            "previous": None,
            "results": serializer.data,
        }
        return Response(response_data)


class OrganizationTypeViewSet(ModelViewSet):
    serializer_class = OrganizationTypeSerializer
    queryset = OrganizationType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrganizationTypeFilter


class OrganizationViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrganizationFilter


class MemberTypeViewSet(ModelViewSet):
    serializer_class = MemberTypeSerializer
    queryset = MemberType.objects.all()


class ConsumerCommitteeDocumentViewSet(ModelViewSet):
    serializer_class = ConsumerCommitteeDocumentSerializer
    queryset = ConsumerCommitteeDocument.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConsumerCommitteeDocumentFilter


class ConsumerCommitteeMemberViewSet(ModelViewSet):
    serializer_class = ConsumerCommitteeMemberSerializer
    queryset = ConsumerCommitteeMember.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConsumerCommitteeMemberFilter


class ConsumerCommitteeViewSet(ModelViewSet):
    serializer_class = ConsumerCommitteeSerializer
    queryset = ConsumerCommittee.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConsumerCommitteeFilter


class MonitoringCommitteeDocumentViewSet(ModelViewSet):
    serializer_class = MonitoringCommitteeDocumentSerializer
    queryset = MonitoringCommitteeDocument.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MonitoringCommitteeDocumentFilter


class MonitoringCommitteeMemberViewSet(ModelViewSet):
    serializer_class = MonitoringCommitteeMemberSerializer
    queryset = MonitoringCommitteeMember.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MonitoringCommitteeMemberFilter


class MonitoringCommitteeViewSet(ModelViewSet):
    serializer_class = MonitoringCommitteeSerializer
    queryset = MonitoringCommittee.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MonitoringCommitteeFilter


class ExecutiveAgencyViewSet(ModelViewSet):
    serializer_class = ExecutiveAgencySerializer
    queryset = ExecutiveAgency.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExecutiveAgencyFilter


class CurrencyViewSet(ModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CurrencyFilter


class ModuleViewSet(ModelViewSet):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()


class SubModuleViewSet(ModelViewSet):
    serializer_class = SubModuleSerializer
    queryset = SubModule.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubModuleFilter


class NewsPaperViewSet(ModelViewSet):
    serializer_class = NewsPaperSerializer
    queryset = NewsPaper.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsPaperFilter


class ProjectStartDecisionViewSet(ModelViewSet):
    serializer_class = ProjectStartDecisionSerializer
    queryset = ProjectStartDecision.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectStartDecisionFilter


class ConstructionMaterialDescriptionViewSet(ModelViewSet):
    serializer_class = ConstructionMaterialDescriptionSerializer
    queryset = ConstructionMaterialDescription.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConstructionMaterialDescriptionFilter


# बजेट तथा स्रोत व्यवस्थापन -->


class BudgetSubTitleViewSet(ModelViewSet):
    serializer_class = BudgetSubTitleSerializer
    queryset = BudgetSubTitle.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BudgetSubTitleFilter


class PaymentMethodViewSet(ModelViewSet):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentMethodFilter


class SourceReceiptViewSet(ModelViewSet):
    serializer_class = SourceReceiptSerializer
    queryset = SourceReceipt.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SourceReceiptFilter


class CollectPaymentViewSet(ModelViewSet):
    serializer_class = CollectPaymentSerializer
    queryset = CollectPayment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectPaymentFilter


class SubLedgerViewSet(ModelViewSet):
    serializer_class = SubLedgerSerializer
    queryset = SubLedger.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubLedgerFilter


class ATMViewSet(ModelViewSet):
    serializer_class = ATMSerializer
    queryset = AccountTitleManagement.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccountTitleManagementFilter

    # @action(methods=["GET"], detail=False)
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter("status", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
    #         openapi.Parameter("name_eng", openapi.IN_QUERY, type=openapi.TYPE_STRING),
    #         openapi.Parameter("module", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    #         openapi.Parameter(
    #             "financial_year", openapi.IN_QUERY, type=openapi.TYPE_INTEGER
    #         ),
    #         openapi.Parameter("parent", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    #     ]
    # )
    # def parent(self, request):
    #     queryset = self.queryset
    #     serializer = self.serializer_class
    #     query_params = request.GET
    #
    #     parent = query_params.get("parent", None)
    #     name_eng = query_params.get("name_eng", None)
    #     module = query_params.get("module", None)
    #     financial_year = query_params.get("financial_year", None)
    #     status = query_params.get("status", None)
    #     limit = query_params.get("limit", None)
    #     offset = query_params.get("offset", 0)
    #     print(limit, 8888888888888888)
    #     if limit in [None, "all", "-1", "0"]:
    #         print(limit, 97238123)
    #         data = AccountTitleManagement.objects.all()
    #         count = data.count()
    #         next_offset = None
    #         prev_offset = None
    #     else:
    #         limit = int(limit) if limit is not None else limit
    #         if int(offset) is None:
    #             raise exceptions.ValidationError({"offset": "Invalid offset"})
    #         offset = int(offset)
    #
    #         if parent is None:
    #             search_fields = Q(module__isnull=True)
    #         else:
    #             search_fields = Q(parent=int(parent))
    #
    #         if name_eng:
    #             search_fields &= Q(name_eng__icontains=name_eng)
    #         if financial_year and int(financial_year) is not None:
    #             search_fields &= Q(financial_year=financial_year)
    #         if module and int(module) is not None:
    #             search_fields &= Q(module=module)
    #         if status is not None and bool(status) is not None:
    #             search_fields &= Q(status=bool(status))
    #
    #         if limit is not None:
    #             hits = queryset.filter(search_fields)[offset: offset + limit]
    #         else:
    #             hits = queryset.filter(search_fields)[offset:]
    #         data = serializer(hits, many=True).data
    #         count = queryset.filter(search_fields).count()
    #         next_offset = offset + limit if limit is not None else None
    #         prev_offset = max(offset - limit, 0) if offset > 0 else None
    #         next_offset = request.build_absolute_uri(f"?offset={next_offset}&limit={limit}")
    #         prev_offset = request.build_absolute_uri(f"?offset={prev_offset}&limit={limit}")
    #     return Response(data={
    #         "count": count,
    #         "next": next_offset if next_offset is not None and count - next_offset > 0 else None,
    #         "previous": prev_offset if prev_offset is not None else None,
    #         "results": data,
    #     }
    #     )
    # def list(self, request, *args, **kwargs):
    #     account_data = AccountTitleManagement.objects.all()
    #     query_params = request.GET
    #     serializer = query_params.get("parent", None)
    #     name_eng = query_params.get("name_eng", None)
    #     module = query_params.get("module", None)
    #     financial_year = query_params.get("financial_year", None)
    #     status = query_params.get("status", None)
    #     limit = query_params.get("limit", None)
    #     offset = query_params.get("offset", 0)
    #     parent = query_params.get("parent", 0)
    #     if limit:
    #         limit = int(limit)
    #         account_data = account_data[:limit]
    #     if parent:
    #         account_data = account_data.filter(parent__id=parent)
    #     elif parent == "":
    #         account_data = account_data.filter(parent__isnull=True)
    #     serializer = ATMSerializer(account_data)
    #     return Response(
    #         data={
    #             "count": account_data.count(),
    #             "next": "",
    #             "previous": "",
    #             "results": serializer.data,
    #         }
    #     )


class BudgetSourceViewSet(ModelViewSet):
    serializer_class = BudgetSourceSerializer
    queryset = BudgetSource.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BudgetSourceFilter


class SBETypeViewSet(ModelViewSet):
    serializer_class = SBETypeSerializer
    queryset = SourceBearerEntityType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SourceBearerEntityTypeFilter


class SBEViewSet(ModelViewSet):
    serializer_class = SBESerializer
    queryset = SourceBearerEntity.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SourceBearerEntityFilter


class DocumentTypeViewSet(ModelViewSet):
    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all()
    filterset_class = DocumentTypeFilter
