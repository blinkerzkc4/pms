# Generated by Django 4.2.1 on 2023-06-06 00:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0012_ratecategory_rate_category"),
        ("log", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="accesslog",
            name="municipality",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.municipality",
            ),
        ),
        migrations.AddField(
            model_name="accesslog",
            name="ward",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.ward",
            ),
        ),
    ]
