# Generated by Django 4.2.1 on 2023-08-17 14:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0038_alter_project_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="quantity",
            name="provisional",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]