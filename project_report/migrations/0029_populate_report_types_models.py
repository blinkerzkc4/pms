from django.db import migrations, models

from project_report.models import ReportType as ReportTypeModel


def populate_report_types(apps, schema_editor):
    ReportType: ReportTypeModel = apps.get_model("project_report", "ReportType")
    report_types = [
        {
            "code": "self_declaration_letter",
            "name_np": "स्वोघोषणा पत्र",
            "text": "Self Declaration Letter",
        },
    ]

    db_alias = schema_editor.connection.alias
    for report_type in report_types:
        ReportType.objects.using(db_alias).create(
            code=report_type["code"],
            name=report_type["name_np"],
            name_eng=report_type["text"],
        )


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0028_populate_report_types_models"),
    ]

    operations = [
        migrations.RunPython(populate_report_types),
    ]
