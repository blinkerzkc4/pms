"""
-- Created by Bikash Saud
-- Created on 2023-07-27
"""

from rest_framework import serializers

from employee.models import Employee
from plan_execution.models import ProjectExecution, ProjectFinishedBailReturn
from pratibedan.report_data import ReportData


class ProjectFinishedBailReturnReportSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExecution.objects.all(), required=False
    )
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__report_data = ReportData()

    class Meta:
        model = ProjectFinishedBailReturn
        fields = (
            "id",
            "project",
            "comment_no",
            "date",
            "date_eng",
            "executive_decision",
            "approved_by",
            "print_custom_report",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "comment_no": {"required": False, "allow_null": True},
            "date": {"required": False, "allow_null": True},
            "date_eng": {"required": False, "allow_null": True},
            "executive_decision": {"required": False, "allow_null": True},
            "approved_by": {"required": False, "allow_null": True},
            "print_custom_report": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        project = instance.project
        # approved_by = instance.approved_by
        project_data = ReportData().get_project_data(project)
        representation["project"] = project_data.dict()
        return representation
