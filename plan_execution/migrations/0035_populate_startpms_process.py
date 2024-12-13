from django.db import migrations, models

from plan_execution.models import StartPmsProcess as StartPmsProcessModel


def populate_start_pms_process(apps, schema_editor):
    StartPmsProcess: StartPmsProcessModel = apps.get_model(
        "plan_execution", "StartPmsProcess"
    )
    pms_processes = [
        {"code": "dp", "name": "अमानत", "name_eng": "Deposit"},
        {
            "code": "institutional",
            "name": "संस्थागत सहकार्य",
            "name_eng": "Institutional Collaboration",
        },
        {"code": "tppt", "name": "ठेक्कापट्ट", "name_eng": "Contract"},
        {"code": "ups", "name": "उपभोक्ता समिति", "name_eng": "Consumer Committee"},
    ]
    db_alias = schema_editor.connection.alias
    for pms_process in pms_processes:
        StartPmsProcess.objects.using(db_alias).create(
            **pms_process,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0034_alter_budgetallocationdetail_expense_title"),
    ]

    operations = [
        migrations.RunPython(populate_start_pms_process),
    ]
