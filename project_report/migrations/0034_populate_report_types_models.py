from django.db import migrations, models

from project_report.models import ReportType as ReportTypeModel


def rename_report_type(apps, schema_editor):
    ReportType: ReportTypeModel = apps.get_model("project_report", "ReportType")
    db_alias = schema_editor.connection.alias
    ReportType.objects.using(db_alias).filter(code="estimate_submit_report").update(
        code="tor_report",
        name="टीओआर रिपोर्ट",
        name_eng="TOR Report",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0033_populate_field_mappings_and_some_codes"),
    ]

    operations = [
        migrations.RunPython(rename_report_type),
    ]
