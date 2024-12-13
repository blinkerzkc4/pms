from django.db import migrations

from project_report.constants.models_for_crt import CRT_MODELS_LIST
from project_report.models import TemplateFieldMapping as TemplateFieldMappingModel
from project_report.models import (
    TemplateFieldMappingGroup as TemplateFieldMappingGroupModel,
)
from utils.report_utils import create_crt_field_names, get_model_fields_old


def populate_custom_report_fields_mapping(apps, schema_editor):
    TemplateFieldMapping: TemplateFieldMappingModel = apps.get_model(
        "project_report", "TemplateFieldMapping"
    )
    TemplateFieldMappingGroup: TemplateFieldMappingGroupModel = apps.get_model(
        "project_report", "TemplateFieldMappingGroup"
    )

    # Getting and storing all the CRT Fields in the Custom Report Template Fields Mapping
    all_crt_fields: list[dict] = []
    already_included_models = set()
    for crt_model in CRT_MODELS_LIST:
        model = apps.get_model(crt_model["app_name"], crt_model["model"])
        fields, already_included_models = get_model_fields_old(
            model,
            already_included_models=already_included_models,
        )
        crt_fields = create_crt_field_names(crt_model["crt_field"], fields)
        all_crt_fields.extend(crt_fields)

    help_text_filtered_crt_fields = [
        {
            "code": crt_field["code"],
            "name": crt_field["name"],
            "name_eng": crt_field["name_eng"],
        }
        for crt_field in all_crt_fields
    ]

    db_alias = schema_editor.connection.alias
    for crt_field in help_text_filtered_crt_fields:
        group, created = TemplateFieldMappingGroup.objects.using(
            db_alias
        ).get_or_create(
            name=crt_field["name"].split(">")[0].strip(" "),
            name_eng=crt_field["name_eng"].split(">")[0].strip(" "),
            code=crt_field["code"].split(".")[0].strip(" "),
        )
        crt_field["group"] = group
        TemplateFieldMapping.objects.using(db_alias).update_or_create(
            code=crt_field["code"],
            defaults=crt_field,
        )


class Migration(migrations.Migration):
    dependencies = [
        (
            "project_report",
            "0015_templatefieldmapping_display_name_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(populate_custom_report_fields_mapping),
    ]
