from django.db import migrations

from project_report.constants.models_for_crt import CRT_MODELS_LIST
from project_report.models import TemplateFieldMapping as TemplateFieldMappingModel
from utils.report_utils import create_crt_field_names, get_model_fields_old


def populate_custom_report_fields_mapping(apps, schema_editor):
    TemplateFieldMapping: TemplateFieldMappingModel = apps.get_model(
        "project_report", "TemplateFieldMapping"
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

    TemplateFieldMapping.objects.using(
        db_alias
    ).all().delete()  # Remove all existing mappings

    TemplateFieldMapping.objects.using(db_alias).bulk_create(
        [
            TemplateFieldMapping(
                **crt_field,
            )
            for crt_field in help_text_filtered_crt_fields
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        (
            "project_report",
            "0013_alter_templatefieldmapping_code_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(populate_custom_report_fields_mapping),
    ]
