# Generated by Django 4.2.3 on 2023-07-12 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0025_estimate_file_alter_estimate_road_1_rate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="unit",
            name="code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]