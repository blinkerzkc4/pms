# Generated by Django 4.2.1 on 2023-10-11 18:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("log", "0004_alter_accesslog_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="accesslog",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
