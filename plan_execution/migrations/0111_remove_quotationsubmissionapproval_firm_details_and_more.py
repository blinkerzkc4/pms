# Generated by Django 4.2.1 on 2024-01-07 05:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0110_alter_quotationfirmdetails_firm_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quotationsubmissionapproval",
            name="firm_details",
        ),
        migrations.AddField(
            model_name="quotationfirmdetails",
            name="submission_approval",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="submission_approval_firm_details",
                to="plan_execution.quotationsubmissionapproval",
            ),
        ),
        migrations.AlterField(
            model_name="firmquotedcostestimate",
            name="cost_estimate_data",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="firm_quoted_cost_estimate",
                to="plan_execution.costestimatedata",
            ),
        ),
    ]