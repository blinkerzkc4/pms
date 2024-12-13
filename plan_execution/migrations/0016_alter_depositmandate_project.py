# Generated by Django 4.2.3 on 2023-07-20 01:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_execution", "0015_alter_depositmandate_report_custom_print"),
    ]

    operations = [
        migrations.AlterField(
            model_name="depositmandate",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="plan_execution.projectexecution",
            ),
        ),
    ]