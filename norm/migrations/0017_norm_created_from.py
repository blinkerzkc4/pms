# Generated by Django 4.2.1 on 2023-08-12 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("norm", "0016_alter_normextracost_on"),
    ]

    operations = [
        migrations.AddField(
            model_name="norm",
            name="created_from",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="norm.norm",
            ),
        ),
    ]
