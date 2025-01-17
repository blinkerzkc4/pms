# Generated by Django 4.2.1 on 2023-08-11 02:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0038_alter_project_name"),
        ("plan_execution", "0026_projecttask"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectexecution",
            name="project",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.project",
            ),
        ),
    ]
