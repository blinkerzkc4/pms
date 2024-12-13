# Generated by Django 4.2.1 on 2023-10-10 01:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0046_update_federal_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="district",
            name="code",
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="municipality",
            name="code",
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="province",
            name="code",
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]