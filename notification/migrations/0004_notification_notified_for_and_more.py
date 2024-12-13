# Generated by Django 4.2.1 on 2023-11-21 01:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notification", "0003_alter_notification_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="notified_for",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="notification",
            name="notified_object",
            field=models.JSONField(blank=True, null=True),
        ),
    ]