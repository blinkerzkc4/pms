# Generated by Django 4.2.1 on 2024-06-01 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notification", "0009_alter_notification_created_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="created_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
