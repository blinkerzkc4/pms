# Generated by Django 4.2.1 on 2023-12-17 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notification", "0005_alter_notification_created_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
