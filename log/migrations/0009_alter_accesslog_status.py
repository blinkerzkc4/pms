# Generated by Django 4.2.1 on 2023-12-17 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("log", "0008_accesslog_actor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accesslog",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]