from django.db import migrations, models

from project_report.views import TemplateFieldMappingViewSet


def delete_old_template_field_mappings(apps, schema_editor):
    TemplateFieldMapping = apps.get_model("project_report", "TemplateFieldMapping")
    db_alias = schema_editor.connection.alias
    TemplateFieldMapping.objects.using(db_alias).all().delete()


#
# TEMPLATE_FIELD_MAPPING_FIELDS = {
#     "ProjectExecution": "all",
#     "ConsumerFormulation": [
#         "first_time_publish",
#         "first_time_publish_eng",
#         "form_amount",
#         "consumer_committee_name",
#         "code",
#         "chariman",
#         "address",
#         "established_date",
#         "phone",
#         "report_date",
#         "report_date_eng",
#         "invoice_no",
#         "project_current_status",
#         "previous_work",
#         "detail_from_office_date",
#         "detail_from_office_date_eng",
#         "opinion",
#         "positive_effect",
#         "othen",
#         "project_related_other",
#         "position",
#     ],
#     "ProbabilityStudyApprove": [
#         "project_selection",
#     ]
# }


def create_new_template_field_mappings(apps, schema_editor):
    crt_fields = TemplateFieldMappingViewSet.get_crt_fields()
    filtered_crt_fields = [
        {
            "code": crt_field["report_code"],
            "name": crt_field["code"],
            "name_eng": crt_field["name_eng"],
            "display_name": crt_field["name"],
            "display_name_eng": crt_field["name_eng"],
            "report_code": crt_field["report_code"],
            "db_column_names": crt_field["db_columns"],
        }
        for crt_field in crt_fields
    ]
    TemplateFieldMapping = apps.get_model("project_report", "TemplateFieldMapping")

    TemplateFieldMappingGroup = apps.get_model(
        "project_report", "TemplateFieldMappingGroup"
    )
    db_alias = schema_editor.connection.alias
    for index, crt_field in enumerate(filtered_crt_fields):
        print(f"CRT Field Number: {index+1}")
        print(crt_field["report_code"])
        if len(crt_field["db_column_names"]) == 1:
            group, created = TemplateFieldMappingGroup.objects.using(
                db_alias
            ).get_or_create(
                name=crt_field["display_name"].split(">")[0].strip(" "),
                name_eng=crt_field["display_name_eng"].split(">")[0].strip(" "),
            )
            crt_field["group"] = group
        TemplateFieldMapping.objects.using(db_alias).update_or_create(
            code=crt_field["code"],
            defaults=crt_field,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0019_templatefieldmapping_report_code"),
    ]

    operations = [
        migrations.RunPython(delete_old_template_field_mappings),
        migrations.RunPython(create_new_template_field_mappings),
    ]
