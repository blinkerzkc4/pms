# Generated by Django 4.2.1 on 2023-11-19 09:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0010_populate_report_types_models"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customreporttemplate",
            name="template_content",
            field=models.TextField(blank=True, null=True),
        ),
    ]
