# Generated by Django 4.2.1 on 2023-06-09 04:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0013_estimationrate_road_1_distance_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estimationrate",
            name="amount",
            field=models.DecimalField(decimal_places=5, max_digits=20),
        ),
        migrations.AlterUniqueTogether(
            name="topic",
            unique_together={("parent", "name_eng", "name_unicode")},
        ),
    ]
