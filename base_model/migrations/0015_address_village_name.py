# Generated by Django 4.2.1 on 2023-12-26 03:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base_model", "0014_alter_contactdetail_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="village_name",
            field=models.CharField(
                blank=True,
                help_text="गाउँको नाम",
                max_length=55,
                null=True,
                verbose_name="Village Name",
            ),
        ),
    ]
