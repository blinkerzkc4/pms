# Generated by Django 4.2.1 on 2023-06-22 12:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0021_remove_estimationrate_estimate_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estimationrate",
            name="amount",
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name="estimationrate",
            name="road_1_distance",
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name="estimationrate",
            name="road_2_distance",
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name="estimationrate",
            name="road_3_distance",
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20),
        ),
    ]
