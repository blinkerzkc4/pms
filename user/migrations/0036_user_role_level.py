# Generated by Django 4.2.1 on 2023-12-30 08:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0035_permission_created_by_permission_created_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role_level",
            field=models.CharField(
                choices=[
                    ("municipality", "Municipality"),
                    ("ward", "Ward"),
                    ("department", "Department"),
                ],
                default="municipality",
                max_length=20,
            ),
        ),
    ]
