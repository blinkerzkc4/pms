# Generated by Django 4.2.1 on 2023-06-09 04:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0014_alter_estimationrate_amount_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="rate",
            name="unit",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.unit",
            ),
        ),
    ]