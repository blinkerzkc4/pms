# Generated by Django 4.2.1 on 2024-01-09 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0117_projectdeadline_site_inspection_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="firmquotedcostestimate",
            name="firm",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="quoted_cost_estimates",
                to="plan_execution.quotationfirmdetails",
            ),
        ),
    ]
