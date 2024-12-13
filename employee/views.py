from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from employee.models import (
    Country,
    CumulativeDetail,
    CurrentWorkingDetail,
    Department,
    DepartmentBranch,
    Employee,
    EmployeeSector,
    EmployeeType,
    EnrollmentDetail,
    FamilyDetail,
    Language,
    MaritalStatus,
    Nationality,
    Position,
    PositionLevel,
    PublicRepresentativeDetail,
    PublicRepresentativePosition,
    Religion,
    ServiceGroup,
    TaxPayer,
)
from employee.serializers import (
    CountrySerializer,
    CumulativeDetailSerializer,
    CurrentWorkingDetailSerializer,
    DepartmentBranchSerializer,
    DepartmentSerializer,
    EmployeeSectorSerializer,
    EmployeeSerializer,
    EmployeeTypeSerializer,
    EmployeeViewSerializer,
    EnrollmentDetailSerializer,
    FamilyDetailSerializer,
    LanguageSerializer,
    MaritalStatusSerializer,
    NationalitySerializer,
    PositionLevelSerializer,
    PositionSerializer,
    PublicRepresentativeDetailSerializer,
    PublicRepresentativePositionSerializer,
    ReligionSerializer,
    ServiceGroupSerializer,
    TaxPayerSerializer,
)
from project_planning.filters import (
    DepartmentFilter,
    EmployeeFilter,
    EmployeeSectorFilter,
    EmployeeTypeFilter,
    PositionFilter,
    PositionLevelFilter,
    PublicRepresentativeDetailFilter,
    PublicRepresentativePositionFilter,
)

# Create your views here.


class MaritalStatusViewSet(ModelViewSet):
    serializer_class = MaritalStatusSerializer
    queryset = MaritalStatus.objects.all()


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepartmentFilter


class DepartmentBranchViewSet(ModelViewSet):
    serializer_class = DepartmentBranchSerializer
    queryset = DepartmentBranch.objects.all()


class PositionLevelViewSet(ModelViewSet):
    serializer_class = PositionLevelSerializer
    queryset = PositionLevel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PositionLevelFilter


class PositionViewSet(ModelViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PositionFilter


class EmployeeTypeViewSet(ModelViewSet):
    serializer_class = EmployeeTypeSerializer
    queryset = EmployeeType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeTypeFilter


class ServiceGroupViewSet(ModelViewSet):
    serializer_class = ServiceGroupSerializer
    queryset = ServiceGroup.objects.all()


class EmployeeSectorViewSet(ModelViewSet):
    serializer_class = EmployeeSectorSerializer
    queryset = EmployeeSector.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeSectorFilter


class CurrentWorkingDetailViewSet(ModelViewSet):
    serializer_class = CurrentWorkingDetailSerializer
    queryset = CurrentWorkingDetail.objects.all()


class FamilyDetailViewSet(ModelViewSet):
    serializer_class = FamilyDetailSerializer
    queryset = FamilyDetail.objects.all()


class EnrollmentDetailViewSet(ModelViewSet):
    serializer_class = EnrollmentDetailSerializer
    queryset = EnrollmentDetail.objects.all()


class CumulativeDetailViewSet(ModelViewSet):
    serializer_class = CumulativeDetailSerializer
    queryset = CumulativeDetail.objects.all()


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EmployeeViewSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = EmployeeViewSerializer(queryset, many=True)
        response_data = {
            "count": len(serializer.data),
            "next": None,
            "previous": None,
            "results": serializer.data,
        }
        return Response(response_data)


class TaxPayerViewSet(ModelViewSet):
    serializer_class = TaxPayerSerializer
    queryset = TaxPayer.objects.all()


class ReligionViewSet(ModelViewSet):
    serializer_class = ReligionSerializer
    queryset = Religion.objects.all()


class LanguageViewSet(ModelViewSet):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


class CountryViewSet(ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class NationalityViewSet(ModelViewSet):
    serializer_class = NationalitySerializer
    queryset = Nationality.objects.all()


class PublicRepresentativePositionViewSet(ModelViewSet):
    serializer_class = PublicRepresentativePositionSerializer
    queryset = PublicRepresentativePosition.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PublicRepresentativePositionFilter


class PublicRepresentativeDetailViewSet(ModelViewSet):
    serializer_class = PublicRepresentativeDetailSerializer
    queryset = PublicRepresentativeDetail.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PublicRepresentativeDetailFilter
