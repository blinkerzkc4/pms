# Generated by Django 4.2.1 on 2023-12-17 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0025_customreporttemplate_required_renders"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customreporttemplate",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="templatefieldmapping",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
