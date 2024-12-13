# Generated by Django 4.1 on 2023-09-03 05:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_execution", "0031_projectphysicaldescription_remarks_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectbidcollection",
            name="bail_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="plan_execution.bailtype",
            ),
        ),
    ]
