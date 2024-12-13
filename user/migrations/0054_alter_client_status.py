# Generated by Django 4.2.1 on 2024-06-17 05:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0053_remove_uuid_null"),
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
                default="ACTIVE",
                max_length=20,
            ),
        ),
    ]
