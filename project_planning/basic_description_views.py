"""
-- Created by Bikash Saud
-- Tech Train Pvt. Ltd.
-- Created on 2023-06-11
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from project_planning.basic_description_serializers import (
    ContractorTypeSerializer,
    DrainageTypeSerializer,
    ExpanseTypeSerializer,
    OfficeSerializer,
    PriorityTypeSerializer,
    ProgramSerializer,
    ProjectActivitySerializer,
    ProjectLevelSerializer,
    ProjectNatureSerializer,
    ProjectProcessSerializer,
    ProjectProposedTypeSerializer,
    ProjectStatusSerializer,
    ProjectTypeSerializer,
    PurchaseTypeSerializer,
    PurposePlanSerializer,
    RoadSerializer,
    RoadStatusSerializer,
    RoadTypeSerializer,
    SelectionFeasibilitySerializer,
    StandingListSerializer,
    StandingListTypeSerializer,
    StrategicSignSerializer,
    TargetGroupCategorySerializer,
    TargetGroupSerializer,
)
from project_planning.models import (
    ContractorType,
    Currency,
    DrainageType,
    ExpanseType,
    Office,
    PriorityType,
    Program,
    ProjectActivity,
    ProjectLevel,
    ProjectNature,
    ProjectProcess,
    ProjectProposedType,
    ProjectStatus,
    ProjectType,
    PurchaseType,
    PurposePlan,
    Road,
    RoadStatus,
    RoadType,
    SelectionFeasibility,
    StandingList,
    StandingListType,
    StrategicSign,
    SubModule,
    TargetGroup,
    TargetGroupCategory,
)

from .filters import *


class ExpanseTypeViewSet(ModelViewSet):
    serializer_class = ExpanseTypeSerializer
    queryset = ExpanseType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpanseTypeFilter


class ProjectTypeViewSet(ModelViewSet):
    serializer_class = ProjectTypeSerializer
    queryset = ProjectType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectTypeFilter


class PurposePlanViewSet(ModelViewSet):
    serializer_class = PurposePlanSerializer
    queryset = PurposePlan.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurposePlanFilter


class ProjectProcessViewSet(ModelViewSet):
    serializer_class = ProjectProcessSerializer
    queryset = ProjectProcess.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectProcessFilter


class ProjectNatureViewSet(ModelViewSet):
    serializer_class = ProjectNatureSerializer
    queryset = ProjectNature.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectNatureFilter


class ProjectLevelViewSet(ModelViewSet):
    serializer_class = ProjectLevelSerializer
    queryset = ProjectLevel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectLevelFilter


class ProjectProposedTypeViewSet(ModelViewSet):
    serializer_class = ProjectProposedTypeSerializer
    queryset = ProjectProposedType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectProposedTypeFilter


class ProjectActivityViewSet(ModelViewSet):
    serializer_class = ProjectActivitySerializer
    queryset = ProjectActivity.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectActivityFilter


class PurchaseTypeViewSet(ModelViewSet):
    serializer_class = PurchaseTypeSerializer
    queryset = PurchaseType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurchaseTypeFilter


class PriorityTypeViewSet(ModelViewSet):
    serializer_class = PriorityTypeSerializer
    queryset = PriorityType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PriorityTypeFilter


class SelectionFeasibilityViewSet(ModelViewSet):
    serializer_class = SelectionFeasibilitySerializer
    queryset = SelectionFeasibility.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SelectionFeasibilityFilter


class StrategicSignViewSet(ModelViewSet):
    serializer_class = StrategicSignSerializer
    queryset = StrategicSign.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StrategicSignFilter


class ProgramViewSet(ModelViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProgramFilter


class TargetGroupCategoryViewSet(ModelViewSet):
    serializer_class = TargetGroupCategorySerializer
    queryset = TargetGroupCategory.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = TargetGroupFilter


class TargetGroupViewSet(ModelViewSet):
    serializer_class = TargetGroupSerializer
    queryset = TargetGroup.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TargetGroupFilter


class ProjectStatusViewSet(ModelViewSet):
    serializer_class = ProjectStatusSerializer
    queryset = ProjectStatus.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectStatusFilter


class ContractTypeViewSet(ModelViewSet):
    serializer_class = ContractorTypeSerializer
    queryset = ContractorType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractorTypeFilter


class OfficeViewSet(ModelViewSet):
    serializer_class = OfficeSerializer
    queryset = Office.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeFilter


# सुचिकृत विवरण operations


class StandingListTypeViewSet(ModelViewSet):
    serializer_class = StandingListTypeSerializer
    queryset = StandingListType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StandingListTypeFilter


class StandingListViewSet(ModelViewSet):
    serializer_class = StandingListSerializer
    queryset = StandingList.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StandingListFilter


class RoadTypeViewSet(ModelViewSet):
    serializer_class = RoadTypeSerializer
    queryset = RoadType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoadTypeFilter


class RoadStatusViewSet(ModelViewSet):
    serializer_class = RoadStatusSerializer
    queryset = RoadStatus.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoadStatusFilter


class DrainageTypeViewSet(ModelViewSet):
    serializer_class = DrainageTypeSerializer
    queryset = DrainageType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = DrainageTypeFilter


class RoadViewSet(ModelViewSet):
    serializer_class = RoadSerializer
    queryset = Road.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoadFilter
