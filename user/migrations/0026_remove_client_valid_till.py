# Generated by Django 4.2.1 on 2023-10-20 06:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0025_remove_user_user_role_user_user_role"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="client",
            name="valid_till",
        ),
    ]
