# Generated by Django 4.2.1 on 2023-10-01 17:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0012_alter_user_user_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("SUPER_ADMIN", "Super Admin"),
                    ("ADMIN", "Admin"),
                    ("MUNICIPALITY_USER", "Municipality User"),
                    ("WARD_USER", "Ward User"),
                ],
                default="SUPER_ADMIN",
                max_length=20,
            ),
        ),
    ]
