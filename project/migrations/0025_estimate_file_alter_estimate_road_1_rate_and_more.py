# Generated by Django 4.2.1 on 2023-07-11 03:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0024_estimate_abstract_of_cost_estimate_district_rate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="estimate",
            name="file",
            field=models.FileField(
                blank=True, null=True, upload_to="uploads/estimate/"
            ),
        ),
        migrations.AlterField(
            model_name="estimate",
            name="road_1_rate",
            field=models.DecimalField(
                blank=True, decimal_places=5, default="0.0", max_digits=20
            ),
        ),
        migrations.AlterField(
            model_name="estimate",
            name="road_2_rate",
            field=models.DecimalField(
                blank=True, decimal_places=5, default="0.0", max_digits=20
            ),
        ),
        migrations.AlterField(
            model_name="estimate",
            name="road_3_rate",
            field=models.DecimalField(
                blank=True, decimal_places=5, default="0.0", max_digits=20
            ),
        ),
    ]
