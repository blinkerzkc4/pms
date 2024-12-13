# Generated by Django 4.2.1 on 2023-12-02 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0046_executiveagency_date_executiveagency_date_eng"),
        ("plan_execution", "0058_alter_projectmobilizationdetail_mobilization"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectexecution",
            name="project_type",
            field=models.ForeignKey(
                blank=True,
                help_text="योजना प्रकार",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="project_executions",
                to="project_planning.projecttype",
                verbose_name="Project Type",
            ),
        ),
    ]