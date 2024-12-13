from django.shortcuts import render
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from plan_execution.models import ProjectExecution, ProjectFinishedBailReturn
from pratibedan.entities import (
    DistrictData,
    MunicipalityData,
    ProvinceData,
    ReportByProjectType,
)
from pratibedan.report_data import ReportData
from pratibedan.serializers import ProjectFinishedBailReturnReportSerializer
from project.models import District, Municipality, Province
from project.serializers import MunicipalitySerializer
from project_planning.models import ProjectType

# Create your views here.


class ContractInvestmentReportAPIView(APIView):
    serializer_class = ProjectFinishedBailReturnReportSerializer

    def get_queryset(self):
        return ProjectFinishedBailReturn.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = ProjectFinishedBailReturnReportSerializer(
            self.get_queryset(), many=True
        )
        response_data = {
            "count": len(serializer.data),
            "next": None,
            "previous": None,
            "results": serializer.data,
        }
        return Response(response_data)


class SchemeBidReportAPIView(APIView):
    pagination_class = PageNumberPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__report_data = ReportData()

    def get_queryset(self):
        return ProjectExecution.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)

        results = []
        for data in result_page:
            project_data = self.__report_data.get_project_data(data)
            results.append(project_data.dict())

        response_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": results,
        }
        return Response(response_data)


class NotCompletedProjectAPIView(APIView):
    pagination_class = PageNumberPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__report_data = ReportData()

    def get(self, request, *args, **kwargs):
        finished_project_ids = ProjectFinishedBailReturn.objects.values_list(
            "project_id", flat=True
        ).distinct()
        finished_projects = ProjectExecution.objects.filter(id__in=finished_project_ids)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(finished_projects, request)

        results = []
        for data in result_page:
            project_data = self.__report_data.get_project_data(data)
            results.append(project_data.dict())

        response_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": results,
        }
        return Response(response_data)


class ProjectsByStartProcessAPIView(APIView):
    pagination_class = PageNumberPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__report_data = ReportData()

    def get(self, request, *args, **kwargs):
        finished_projects = ProjectExecution.objects.exclude(start_pms_process=None)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(finished_projects, request)
        results = []
        for data in result_page:
            project_data = self.__report_data.get_project_data(data)
            results.append(project_data.dict())

        response_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": results,
        }
        return Response(response_data)


class ByProjectLevelAPIView(APIView):
    pagination_class = PageNumberPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__report_data = ReportData()

    def get(self, request, *args, **kwargs):
        try:
            projects = ProjectExecution.objects.exclude(project_level=None)
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(projects, request)
            results = []
            for data in result_page:
                project_data = self.__report_data.get_project_new_report(data)
                results.append(project_data.dict())
            response_data = {
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "results": results,
            }
            return Response(response_data)
        except Exception as e:
            raise e


class ByProjectTypeAPIView(APIView):
    """
    HELP TEXT:
    Not ProjectType: Karya kshatra:
    as data
    shown {work_proposer_type_name	"अन्य"} in
    http://yojana.shangrilagroup.com.np/api/plan_master?_dc=1690630799254&pms_process_id=2&flag=YojanaTypeReport&page=1&start=0&limit=999999
    """

    pagination_class = PageNumberPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__report_data = ReportData()
        self.__project_type_data = ReportByProjectType()

    def get(self, request, *args, **kwargs):
        try:
            project_types = ProjectType.objects.prefetch_related(
                "project_executions__project_unit__unit_type"
            )
            response_data = []
            for project_type in project_types:
                not_completed_unit_count = 0
                completed_unit_count = 0

                project_type_data = {}
                project_executions = project_type.projectexecution_set.all()
                for project_execution in project_executions:
                    units = project_execution.project_unit.all()
                    for unit in units:
                        complete_finish = ProjectFinishedBailReturn.objects.filter(
                            project=project_execution
                        )
                        if complete_finish:
                            completed_unit_count += int(unit.unit)
                        else:
                            not_completed_unit_count += int(unit.unit)
                        project_type_data["project_type"] = project_type.name
                        # unit_data = [unit.unit_type.name for unit in units]
                        project_type_data["units"] = unit.unit_type.name
                        project_type_data[
                            "completed_project_unit_count"
                        ] = completed_unit_count
                        project_type_data[
                            "not_completed_project_unit_count"
                        ] = not_completed_unit_count
                if len(project_type_data) > 0:
                    response_data.append(project_type_data)
            return Response(response_data)
        except Exception as e:
            raise e


class ByProjectSubjectArea(APIView):
    pagination_class = PageNumberPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__report_data = ReportData()

    def get(self, request, *args, **kwargs):
        finished_projects = ProjectExecution.objects.exclude(subject_area=None)
        print(finished_projects, 8172987213)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(finished_projects, request)
        results = []
        for data in result_page:
            project_data = self.__report_data.get_project_by_subject_area(data)
            results.append(project_data.dict())
        response_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": results,
        }
        return Response(response_data)


class ByAgreementAPIView(APIView):
    pagination_class = PageNumberPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__report_data = ReportData()

    def get(self, request, *args, **kwargs):
        finished_projects = ProjectExecution.objects.exclude(start_pms_process=None)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(finished_projects, request)
        results = []
        for data in result_page:
            project_data = self.__report_data.get_project_by_agreement(data)
            results.append(project_data.dict())
        response_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": results,
        }
        return Response(response_data)


class ByPaymentDetailAPIView(APIView):
    pagination_class = PageNumberPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__report_data = ReportData()

    def get(self, request, *args, **kwargs):
        finished_projects = ProjectExecution.objects.exclude(start_pms_process=None)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(finished_projects, request)
        results = []
        for data in result_page:
            project_data = self.__report_data.get_project_by_payment_detail(data)
            results.append(project_data.dict())
        response_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": results,
        }
        return Response(response_data)


class ByPhysicalProgressAPIView(APIView):
    pagination_class = PageNumberPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__report_data = ReportData()

    def get(self, request, *args, **kwargs):
        finished_projects = ProjectExecution.objects.exclude(start_pms_process=None)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(finished_projects, request)
        results = []
        for data in result_page:
            project_data = self.__report_data.get_project_data(data)
            results.append(project_data.dict())
        response_data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": results,
        }
        return Response(response_data)


class AddressLineAPIView(APIView):
    def get(self, request, *args, **kwargs):
        provinces = Province.objects.all()
        results = []
        for province in provinces:
            province_data = ProvinceData()
            province_data.districts = self.get_district_data(province)
            province_data.id = province.id
            province_data.province_number = province.province_number
            province_data.name = province.name
            province_data.name_unicode = province.name_unicode
            province_data.name_eng = province.name_eng
            province_data.remarks = province.remarks
            results.append(province_data.dict())
        response_data = {
            "count": provinces.count(),
            "next": None,
            "previous": None,
            "results": results,
        }
        return Response(response_data)

    def get_district_data(self, province):
        try:
            districts_list = []
            districts = District.objects.filter(province=province)
            for district in districts:
                district_data = DistrictData()
                district_data.id = district.id
                district_data.name = district.name
                district_data.name_eng = district.name_eng
                district_data.name_unicode = district.name_unicode
                district_data.municipalities = self.get_municipality_data(district)
                districts_list.append(district_data)
            return districts_list
        except Exception as e:
            print(f"Exception to get district data: {e}")
            return []

    @staticmethod
    def get_municipality_data(district):
        try:
            municipalities_list = []
            municipalities = Municipality.objects.filter(district=district)
            for municipality in municipalities:
                municipality_data = MunicipalityData()
                municipality_data.id = municipality.id
                municipality_data.name = municipality.name
                municipality_data.name_eng = municipality.name_eng
                municipality_data.name_unicode = municipality.name_unicode
                municipality_data.number_of_wards = municipality.number_of_wards
                municipality_data.remarks = municipality.remarks
                municipality_data.email = municipality.email
                municipality_data.phone = municipality.phone
                municipalities_list.append(municipality_data)
            return municipalities_list
        except Exception as e:
            print(f"Exception to get municipality data: {e}")
            return []


class MunicipalityAddressAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            municipality = Municipality.objects.filter(
                id=user.assigned_municipality.id
            ).first()
            mun_data = MunicipalitySerializer(municipality)
            return Response(mun_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Exception: {e}")
            return Response(
                {"success": False, "message": "Unable to get current Address"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
