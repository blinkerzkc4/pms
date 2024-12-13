# Generated by Django 4.2.1 on 2023-11-23 18:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project_report", "0011_alter_customreporttemplate_template_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reporttype",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=55,
                null=True,
                verbose_name="Code",
            ),
        ),
        migrations.AlterField(
            model_name="reporttype",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="reporttype",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="reporttype",
            name="detail",
            field=models.CharField(
                blank=True,
                help_text="विवरण",
                max_length=500,
                null=True,
                verbose_name="Detail",
            ),
        ),
        migrations.AlterField(
            model_name="reporttype",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="नाम",
                max_length=100,
                null=True,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="reporttype",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=100,
                null=True,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="reporttype",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="reporttype",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="templatefieldmapping",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=55,
                null=True,
                verbose_name="Code",
            ),
        ),
        migrations.AlterField(
            model_name="templatefieldmapping",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="templatefieldmapping",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="templatefieldmapping",
            name="detail",
            field=models.CharField(
                blank=True,
                help_text="विवरण",
                max_length=500,
                null=True,
                verbose_name="Detail",
            ),
        ),
        migrations.AlterField(
            model_name="templatefieldmapping",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="नाम",
                max_length=100,
                null=True,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="templatefieldmapping",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=100,
                null=True,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="templatefieldmapping",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
    ]
