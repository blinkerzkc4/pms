# Generated by Django 4.2.1 on 2024-06-01 18:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("norm", "0028_norm_part_activity_no_norm_part_specification_no_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="norm",
            name="remarks",
            field=models.TextField(blank=True, default="", null=True),
        ),
    ]