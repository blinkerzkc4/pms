# Generated by Django 4.2.1 on 2023-05-16 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0004_alter_muncipality_options_rate_muncipality_and_more"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="assigned_muncipality",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.muncipality",
            ),
        ),
    ]
