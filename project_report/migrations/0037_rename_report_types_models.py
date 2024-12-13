from django.db import migrations, models

from project_report.models import ReportType as ReportTypeModel


def rename_report_type(apps, schema_editor):
    ReportType: ReportTypeModel = apps.get_model("project_report", "ReportType")
    db_alias = schema_editor.connection.alias
    ReportType.objects.using(db_alias).filter(code="estimate_submit_report").update(
        code="last_payment_report",
        name="अन्तिम भुक्तानी",
        name_eng="Final Payment",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0036_populate_report_types_models"),
    ]

    operations = [
        migrations.RunPython(rename_report_type),
    ]
