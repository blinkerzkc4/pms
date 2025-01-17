# Generated by Django 4.2.1 on 2024-01-17 05:20

from django.db import migrations

from plan_execution.models import OpeningContractAccount as OpeningContractAccountModel


def update_blank_values_in_oca_mandate_employee(apps, schema_editor):
    OpeningContractAccount: OpeningContractAccountModel = apps.get_model(
        "plan_execution", "OpeningContractAccount"
    )
    db_alias = schema_editor.connection.alias
    for oca in OpeningContractAccount.objects.using(db_alias).filter(
        mandate_employee=""
    ):
        oca.mandate_employee = None
        oca.save()
    for oca in OpeningContractAccount.objects.using(db_alias).filter(
        mandate_employee_position=""
    ):
        oca.mandate_employee_position = None
        oca.save()


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0124_update_installment_model_again"),
    ]

    operations = [
        migrations.RunPython(
            update_blank_values_in_oca_mandate_employee,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
