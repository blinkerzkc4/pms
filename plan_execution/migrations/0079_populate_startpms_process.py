from django.db import migrations, models

from plan_execution.models import StartPmsProcess as StartPmsProcessModel


def populate_start_pms_process(apps, schema_editor):
    StartPmsProcess: StartPmsProcessModel = apps.get_model(
        "plan_execution", "StartPmsProcess"
    )
    pms_processes = [
        {"code": "quot", "name": "उद्धरण", "name_eng": "Quotation"},
    ]
    db_alias = schema_editor.connection.alias
    for pms_process in pms_processes:
        StartPmsProcess.objects.using(db_alias).create(
            **pms_process,
        )


class Migration(migrations.Migration):
    dependencies = [
        (
            "plan_execution",
            "0078_alter_projectagreement_office_witness_1_position_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(populate_start_pms_process),
    ]
