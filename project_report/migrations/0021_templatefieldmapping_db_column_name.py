# Generated by Django 4.2.1 on 2023-12-14 05:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0020_new_custom_report_fields_mapping"),
    ]

    operations = [
        migrations.AddField(
            model_name="templatefieldmapping",
            name="db_column_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]