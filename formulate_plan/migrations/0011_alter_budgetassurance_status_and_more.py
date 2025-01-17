# Generated by Django 4.2.1 on 2023-10-11 18:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formulate_plan", "0010_alter_workproject_project_level"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budgetassurance",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="projectdocument",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="projectworktype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="workclass",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
