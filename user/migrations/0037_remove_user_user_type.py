# Generated by Django 4.2.1 on 2023-12-30 09:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0036_user_role_level"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="user_type",
        ),
    ]
