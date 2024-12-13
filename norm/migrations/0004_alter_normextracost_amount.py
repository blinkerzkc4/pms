# Generated by Django 4.2.1 on 2023-06-15 13:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("norm", "0003_remove_norm_extra_costs_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="normextracost",
            name="amount",
            field=models.DecimalField(decimal_places=5, default="0.0", max_digits=20),
        ),
    ]