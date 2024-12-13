# Generated by Django 4.2.1 on 2023-07-10 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0024_estimate_abstract_of_cost_estimate_district_rate_and_more"),
        ("norm", "0011_rename_part_norm_item_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="normcomponent",
            name="municipality",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.municipality",
            ),
        ),
        migrations.AddField(
            model_name="normextracost",
            name="municipality",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.municipality",
            ),
        ),
    ]