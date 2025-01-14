# Generated by Django 4.2.1 on 2023-12-30 03:04

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app_settings", "0003_alter_booleanappsetting_setting_collection_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appsettingcollection",
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
        migrations.AddField(
            model_name="appsettingcollection",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                help_text="निर्माण मिति",
                verbose_name="Created Date",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="appsettingcollection",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AddField(
            model_name="appsettingcollection",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AddField(
            model_name="booleanappsetting",
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
        migrations.AddField(
            model_name="booleanappsetting",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                help_text="निर्माण मिति",
                verbose_name="Created Date",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="booleanappsetting",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AddField(
            model_name="booleanappsetting",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AddField(
            model_name="imageappsetting",
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
        migrations.AddField(
            model_name="imageappsetting",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                help_text="निर्माण मिति",
                verbose_name="Created Date",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="imageappsetting",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AddField(
            model_name="imageappsetting",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
    ]
