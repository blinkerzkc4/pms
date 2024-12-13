# Generated by Django 4.2.1 on 2024-01-09 01:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employee", "0020_cumulativedetail_code_currentworkingdetail_code_and_more"),
        ("plan_execution", "0113_paymentexitbill_payment_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectdeadline",
            name="cha_no",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="projectdeadline",
            name="letter_no",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="projectdeadline",
            name="site_inspector",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="deadline_sites_inspected",
                to="employee.employee",
            ),
        ),
        migrations.AddField(
            model_name="projectdeadline",
            name="site_inspector_position",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="deadline_sites_inspected",
                to="employee.employeesector",
            ),
        ),
        migrations.AlterField(
            model_name="projectdeadline",
            name="decision_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="deadline_extensions_decided",
                to="employee.employee",
            ),
        ),
    ]
