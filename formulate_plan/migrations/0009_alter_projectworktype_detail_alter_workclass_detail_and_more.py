# Generated by Django 4.2.3 on 2023-07-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("formulate_plan", "0008_rename_is_prioritization_workproject_is_prioritized"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectworktype",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="workclass",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
