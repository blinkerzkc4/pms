# Generated by Django 4.2.1 on 2023-10-17 17:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0023_remove_userrole_districtrate_create_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("SUSPENDED", "Suspended"),
                    ("ACTIVE", "Active"),
                    ("PENDING", "Pending"),
                ],
                default="PENDING",
                max_length=20,
            ),
        ),
    ]
