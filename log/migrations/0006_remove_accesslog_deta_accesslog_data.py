# Generated by Django 4.2.1 on 2023-11-10 03:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("log", "0005_accesslog_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="accesslog",
            name="deta",
        ),
        migrations.AddField(
            model_name="accesslog",
            name="data",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
