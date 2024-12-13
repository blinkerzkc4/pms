# Generated by Django 4.2.1 on 2023-06-13 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "project_planning",
            "0019_road_drainage_exit_status_road_drainage_length_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="bfi",
            name="code",
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AddField(
            model_name="bfi",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="bfi",
            name="name_eng",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]