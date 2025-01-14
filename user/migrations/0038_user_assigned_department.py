# Generated by Django 4.2.1 on 2023-12-30 09:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employee", "0019_alter_currentworkingdetail_status_and_more"),
        ("user", "0037_remove_user_user_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="assigned_department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="employee.department",
            ),
        ),
    ]
