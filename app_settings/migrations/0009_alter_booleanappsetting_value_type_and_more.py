# Generated by Django 4.2.1 on 2024-01-08 09:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app_settings", "0008_appsettingcollection_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booleanappsetting",
            name="value_type",
            field=models.CharField(
                choices=[
                    ("string", "String"),
                    ("integer", "Integer"),
                    ("float", "Float"),
                    ("boolean", "Boolean"),
                    ("image", "Image"),
                    ("file", "File"),
                    ("enum", "Enum"),
                ],
                default="boolean",
                editable=False,
                help_text="मान प्रकार",
                max_length=55,
                verbose_name="Value Type",
            ),
        ),
        migrations.AlterField(
            model_name="imageappsetting",
            name="value_type",
            field=models.CharField(
                choices=[
                    ("string", "String"),
                    ("integer", "Integer"),
                    ("float", "Float"),
                    ("boolean", "Boolean"),
                    ("image", "Image"),
                    ("file", "File"),
                    ("enum", "Enum"),
                ],
                default="image",
                editable=False,
                help_text="मान प्रकार",
                max_length=55,
                verbose_name="Value Type",
            ),
        ),
        migrations.AlterField(
            model_name="integerappsetting",
            name="value_type",
            field=models.CharField(
                choices=[
                    ("string", "String"),
                    ("integer", "Integer"),
                    ("float", "Float"),
                    ("boolean", "Boolean"),
                    ("image", "Image"),
                    ("file", "File"),
                    ("enum", "Enum"),
                ],
                default="integer",
                editable=False,
                help_text="मान प्रकार",
                max_length=55,
                verbose_name="Value Type",
            ),
        ),
        migrations.CreateModel(
            name="EnumAppSetting",
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
                    "setting_type",
                    models.CharField(
                        choices=[("general", "General"), ("yojana", "Yojana")],
                        default="general",
                        help_text="सेटिङ्ग प्रकार",
                        max_length=55,
                        verbose_name="Setting Type",
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
                    "use_in_report",
                    models.BooleanField(
                        default=False,
                        help_text="रिपोर्टमा प्रयोग गर्नुहोस्",
                        verbose_name="Use in Report",
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        blank=True,
                        help_text="मान",
                        max_length=55,
                        null=True,
                        verbose_name="Value",
                    ),
                ),
                (
                    "value_type",
                    models.CharField(
                        choices=[
                            ("string", "String"),
                            ("integer", "Integer"),
                            ("float", "Float"),
                            ("boolean", "Boolean"),
                            ("image", "Image"),
                            ("file", "File"),
                            ("enum", "Enum"),
                        ],
                        default="enum",
                        editable=False,
                        help_text="मान प्रकार",
                        max_length=55,
                        verbose_name="Value Type",
                    ),
                ),
                (
                    "options",
                    models.JSONField(
                        blank=True,
                        help_text="विकल्पहरू",
                        null=True,
                        verbose_name="Options",
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
                (
                    "setting_collection",
                    models.ForeignKey(
                        help_text="सेटिङ्ग संग्रह",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="enum_app_settings",
                        to="app_settings.appsettingcollection",
                        verbose_name="Setting Collection",
                    ),
                ),
            ],
            options={
                "verbose_name": "Enum App Setting",
                "verbose_name_plural": "Enum App Settings",
            },
        ),
    ]
