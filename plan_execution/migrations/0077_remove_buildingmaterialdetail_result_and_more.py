# Generated by Django 4.2.1 on 2023-12-16 08:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0076_alter_buildingmaterialdetail_material"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="buildingmaterialdetail",
            name="result",
        ),
        migrations.AddField(
            model_name="buildingmaterialdetail",
            name="amount",
            field=models.CharField(
                blank=True,
                help_text="परिमाण",
                max_length=255,
                null=True,
                verbose_name="Amount",
            ),
        ),
    ]
