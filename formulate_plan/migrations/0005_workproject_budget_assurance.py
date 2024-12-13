# Generated by Django 4.2.1 on 2023-07-02 02:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("formulate_plan", "0004_workproject_project_level"),
    ]

    operations = [
        migrations.AddField(
            model_name="workproject",
            name="budget_assurance",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="formulate_plan.budgetassurance",
            ),
        ),
    ]
