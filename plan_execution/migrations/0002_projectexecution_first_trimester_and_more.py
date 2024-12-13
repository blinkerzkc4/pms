# Generated by Django 4.2.1 on 2023-07-05 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_execution", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectexecution",
            name="first_trimester",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="projectexecution",
            name="fourth_trimester",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="projectexecution",
            name="second_trimester",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="projectexecution",
            name="third_trimester",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]