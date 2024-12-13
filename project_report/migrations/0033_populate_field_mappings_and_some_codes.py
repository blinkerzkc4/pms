import csv

from django.db import migrations, models

from project_report.models import ReportType as ReportTypeModel
from project_report.models import TemplateFieldMapping as TemplateFieldMappingModel
from project_report.models import (
    TemplateFieldMappingGroup as TemplateFieldMappingGroupModel,
)


def get_field_mapping_model(apps) -> TemplateFieldMappingModel:
    return apps.get_model("project_report", "TemplateFieldMapping")


def populate_measuing_book_field_mappings(apps, schema_editor):
    TemplateFieldMapping = get_field_mapping_model(apps)
    TemplateFieldMappingGroup: TemplateFieldMappingGroupModel = apps.get_model(
        "project_report", "TemplateFieldMappingGroup"
    )
    db_alias = schema_editor.connection.alias
    measuring_book_field_mappings_group = (
        TemplateFieldMappingGroup.objects.using(db_alias)
        .filter(code="measuring_book")
        .first()
    )

    with open(
        "project_report/data/measuring_book_field_mapping_data.csv",
        "r",
        encoding="utf-8-sig",
    ) as deposit_mandate_field_mappings:
        reader = csv.DictReader(deposit_mandate_field_mappings)
        for row in reader:
            TemplateFieldMapping.objects.using(db_alias).create(
                code=row["code"],
                name=row["name nepali"],
                name_eng=row["name"],
                group=measuring_book_field_mappings_group,
            )


def populate_report_types(apps, schema_editor):
    ReportType: ReportTypeModel = apps.get_model("project_report", "ReportType")
    db_alias = schema_editor.connection.alias
    report_types = [
        {
            "code": "regarding_consumer_formulation",
            "name_np": "उपभोक्ता गठन सम्बन्धमा",
            "text": "Regarding User Committee Formulation",
        },
    ]

    for report_type in report_types:
        if (
            not ReportType.objects.using(db_alias)
            .filter(
                code=report_type["code"],
            )
            .exists()
        ):
            ReportType.objects.using(db_alias).create(
                code=report_type["code"],
                name=report_type["name_np"],
                name_eng=report_type["text"],
            )


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0032_populate_field_mappings_and_some_codes"),
    ]

    operations = [
        migrations.RunPython(populate_report_types),
        migrations.RunPython(populate_measuing_book_field_mappings),
    ]
