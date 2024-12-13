from django.db import migrations, models

from project_report.models import ReportType as ReportTypeModel


def populate_report_types(apps, schema_editor):
    ReportType: ReportTypeModel = apps.get_model("project_report", "ReportType")
    report_types = [
        {
            "code": "last_payment_report",
            "name_np": "अन्तिम भुक्तानी",
            "text": "Final Payment",
        },
        {
            "code": "project_request_letter",
            "name_np": "योजना माग निवेदन",
            "text": "Planning Request Application",
        },
        {
            "code": "tole_member_yojana_request_letter",
            "name_np": "योजना माग गर्ने टोलबासीहरुको विवरण",
            "text": "Details of villagers requesting the plan",
        },
    ]

    db_alias = schema_editor.connection.alias
    for report_type in report_types:
        ReportType.objects.using(db_alias).update_or_create(
            code=report_type["code"],
            defaults={
                "name": report_type["name_np"],
                "name_eng": report_type["text"],
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0035_populate_report_types_models"),
    ]

    operations = [
        migrations.RunPython(populate_report_types),
    ]
