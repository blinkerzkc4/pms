# Generated by Django 4.2.1 on 2023-07-30 03:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("norm", "0014_norm_project"),
        ("project", "0029_alter_estimate_project"),
    ]

    operations = [
        migrations.AddField(
            model_name="estimationrate",
            name="norm",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="norm.norm",
            ),
        ),
        migrations.AlterField(
            model_name="quantity",
            name="type",
            field=models.CharField(
                choices=[
                    ("PART", "Part"),
                    ("SUB_PART", "Sub Part"),
                    ("ITEM", "Item"),
                    ("TOTAL", "Total"),
                ],
                max_length=20,
            ),
        ),
    ]