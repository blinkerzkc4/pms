# Generated by Django 4.2.1 on 2023-12-17 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base_model", "0013_populate_gender_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactdetail",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
