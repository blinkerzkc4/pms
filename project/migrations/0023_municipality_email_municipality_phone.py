# Generated by Django 4.2.1 on 2023-07-04 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0022_alter_estimationrate_amount_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="municipality",
            name="email",
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="municipality",
            name="phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
