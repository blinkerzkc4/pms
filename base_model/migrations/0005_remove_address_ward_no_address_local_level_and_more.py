# Generated by Django 4.2.1 on 2023-06-12 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "base_model",
            "0004_remove_address_district_remove_address_local_level_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="address",
            name="ward_no",
        ),
        migrations.AddField(
            model_name="address",
            name="local_level",
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AddField(
            model_name="address",
            name="ward",
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
