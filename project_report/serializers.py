from rest_framework import serializers

from base_model.base_serializers import CommonSerializer
from plan_execution.models import StartPmsProcess
from plan_execution.serializers import StartPmsProcessSerializer
from project_planning.models import ProjectProcess

from .models import (
    CustomReportTemplate,
    ReportType,
    TemplateFieldMapping,
    TemplateFieldMappingGroup,
)


class TemplateFieldMappingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateFieldMappingGroup
        fields = (
            "name",
            "name_eng",
            "code",
            "status",
            "id",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class TemplateFieldMappingSerializer(serializers.ModelSerializer):
    pms_process_id = serializers.PrimaryKeyRelatedField(
        queryset=StartPmsProcess.objects.all(), required=False, allow_null=True
    )
    group = serializers.PrimaryKeyRelatedField(
        queryset=TemplateFieldMappingGroup.objects.all(),
        required=False,
        allow_null=True,
    )
    deleted_by = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    deleted_on = serializers.DateTimeField(read_only=True, allow_null=True)
    updated_by = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    is_deleted = serializers.BooleanField(read_only=True, allow_null=True)

    class Meta:
        fields = (
            "code",
            "name",
            "name_eng",
            "detail",
            "created_by",
            "created_date",
            "updated_date",
            "group",
            "display_name",
            "display_name_eng",
            "status",
            "is_deleted",
            "deleted_by",
            "deleted_on",
            "updated_by",
            "pms_process_id",
            "client_ward",
            "report_code",
            "client_id",
            "process_name",
            "default_value",
            "remarks",
            "id",
        )
        extra_kwargs = {
            "code": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
            "created_by": {"required": False, "allow_null": True},
            "created_date": {"required": False, "allow_null": True},
            "updated_date": {"required": False, "allow_null": True},
            "group": {"required": False, "allow_null": True},
            "display_name": {"required": False, "allow_null": True},
            "display_name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "report_code": {"read_only": True},
            "is_deleted": {"required": False, "allow_null": True},
            "deleted_by": {"required": False, "allow_null": True},
            "deleted_on": {"required": False, "allow_null": True},
            "updated_by": {"required": False, "allow_null": True},
            "pms_process_id": {"required": False, "allow_null": True},
            "client_ward": {"required": False, "allow_null": True},
            "client_id": {"required": False, "allow_null": True},
            "process_name": {"required": False, "allow_null": True},
            "default_value": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
        }
        model = TemplateFieldMapping

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        pms_process_id = instance.pms_process_id
        process_name = instance.process_name
        group = instance.group
        if group:
            representation["group"] = TemplateFieldMappingGroupSerializer(group).data

        if not process_name and pms_process_id:
            representation["process_name"] = pms_process_id.name
        if pms_process_id:
            representation["pms_process_id"] = self.get_pms_process(pms_process_id)
        return representation

    def get_pms_process(self, data):
        return {
            "id": data.id,
            "name": data.name,
            "name_eng": data.name_eng,
        }


class CustomReportTemplateSeralizer(serializers.ModelSerializer):
    template_type_name = serializers.CharField(read_only=True)
    process_type_name = serializers.CharField(read_only=True)
    name = serializers.CharField(required=True)
    name_eng = serializers.CharField(required=True)

    class Meta:
        model = CustomReportTemplate
        fields = (
            "client_id",
            "template_type_id",
            "plan_master_id",
            "name_eng",
            "name",
            "description",
            "orientation",
            "template_info",
            "client_ward",
            "is_report_header_show",
            "status",
            "is_locked",
            "start_pms_process",
            "is_ward_template",
            "is_new_template",
            "template_type_name",
            "process_type_name",
            "id",
            "is_template_default",
            "plan_master_id",
            "template_content",
        )
        extra_kwargs = {
            "client_id": {"required": False, "allow_null": True},
            "template_type_id": {"required": False, "allow_null": True},
            "plan_master_id": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "description": {"required": False, "allow_null": True},
            "orientation": {"required": False, "allow_null": True},
            "template_info": {"required": False, "allow_null": True},
            "client_ward": {"required": False, "allow_null": True},
            "is_report_header_show": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "start_pms_process": {"required": False, "allow_null": True},
            "is_ward_template": {"required": False, "allow_null": True},
            "is_new_template": {"required": False, "allow_null": True},
            "template_type_name": {"required": False, "allow_null": True},
            "process_type_name": {"required": False, "allow_null": True},
            "is_template_default": {"required": False, "allow_null": True},
            "plan_master_id": {"required": False, "allow_null": True},
            "template_content": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        template_type_id = instance.template_type_id
        start_pms_process = instance.start_pms_process

        if template_type_id is not None:
            representation["template_type_name"] = instance.template_type_id.name
        if start_pms_process is not None:
            representation["process_type_name"] = instance.start_pms_process.name

        return representation


class ReportTypeSeralizer(serializers.ModelSerializer):
    code = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    name_eng = serializers.CharField(required=True)
    text = serializers.CharField(read_only=True)

    class Meta:
        fields = [
            "name",
            "name_eng",
            "code",
            "text",
            "id",
            "status",
        ]
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "text": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        model = ReportType

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["text"] = f'{representation["code"]} - {representation["name"]}'
        return representation
