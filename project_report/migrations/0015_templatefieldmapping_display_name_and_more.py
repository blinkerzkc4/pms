# Generated by Django 4.2.1 on 2023-12-03 05:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project_report", "0014_populate_custom_report_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="templatefieldmapping",
            name="display_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="templatefieldmapping",
            name="display_name_eng",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name="TemplateFieldMappingGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="निर्माण मिति",
                        verbose_name="Created Date",
                    ),
                ),
                (
                    "updated_date",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="अद्यावधिक मिति",
                        verbose_name="Updated Date",
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=True, help_text="स्थिति", verbose_name="Status"
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        blank=True,
                        help_text="कोड",
                        max_length=55,
                        null=True,
                        verbose_name="Code",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="नाम",
                        max_length=100,
                        null=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "name_eng",
                    models.CharField(
                        blank=True,
                        help_text="नाम (अंग्रेजी)",
                        max_length=100,
                        null=True,
                        verbose_name="Name (Eng)",
                    ),
                ),
                (
                    "detail",
                    models.CharField(
                        blank=True,
                        help_text="विवरण",
                        max_length=500,
                        null=True,
                        verbose_name="Detail",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="निर्माण गर्ने",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="templatefieldmapping",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="template_field_mappings",
                to="project_report.templatefieldmappinggroup",
            ),
        ),
    ]