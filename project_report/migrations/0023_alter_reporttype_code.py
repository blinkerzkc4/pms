# Generated by Django 4.2.1 on 2023-12-17 01:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0022_populate_report_types_models"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reporttype",
            name="code",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
