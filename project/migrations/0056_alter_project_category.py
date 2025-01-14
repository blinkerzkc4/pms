# Generated by Django 4.2.1 on 2023-12-02 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0055_alter_district_code_alter_district_created_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="category",
            field=models.ForeignKey(
                blank=True,
                help_text="श्रेणी",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="projects",
                to="project.projectcategory",
                verbose_name="Category",
            ),
        ),
    ]
