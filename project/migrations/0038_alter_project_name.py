# Generated by Django 4.2.1 on 2023-08-11 02:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0037_quantity_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="name",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
