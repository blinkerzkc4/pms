# Generated by Django 4.2.1 on 2023-12-02 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "plan_execution",
            "0057_remove_usercommitteemonitoring_monitor_committee_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectmobilizationdetail",
            name="mobilization",
            field=models.ForeignKey(
                help_text="योजना संचालन",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mobilization_details",
                to="plan_execution.projectmobilization",
                verbose_name="Project Mobilization",
            ),
        ),
    ]
