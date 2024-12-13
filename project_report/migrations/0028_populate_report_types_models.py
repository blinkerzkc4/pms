from django.db import migrations, models

from project_report.models import ReportType as ReportTypeModel


def populate_report_types(apps, schema_editor):
    ReportType: ReportTypeModel = apps.get_model("project_report", "ReportType")
    report_types = [
        {
            "code": "quotation_specification_report",
            "name_np": "उद्धरण विवरण रिपोर्ट",
            "text": "Quotation Specification Report",
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
        ("project_report", "0027_customreporttemplate_is_locked"),
    ]

    operations = [
        migrations.RunPython(populate_report_types),
    ]
