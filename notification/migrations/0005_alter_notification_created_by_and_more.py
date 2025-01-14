# Generated by Django 4.2.1 on 2023-11-23 18:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notification", "0004_notification_notified_for_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
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
            model_name="notification",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
    ]
