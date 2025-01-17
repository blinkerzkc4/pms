# Generated by Django 4.2.1 on 2024-02-02 08:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0128_consumerformulation_monitor_committee_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectunitdetail",
            name="total_unit",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="projectunitdetail",
            name="unit",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="projectunitdetail",
            name="unit_rate",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
