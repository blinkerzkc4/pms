# Generated by Django 4.2.3 on 2023-08-19 03:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project_planning", "0029_rename_text_submodule_remarks"),
    ]

    operations = [
        migrations.AddField(
            model_name="submodule",
            name="module",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="project_planning.module",
            ),
        ),
    ]
