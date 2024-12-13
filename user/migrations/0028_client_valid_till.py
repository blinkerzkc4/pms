# Generated by Django 4.2.1 on 2023-11-02 06:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0027_alter_user_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="valid_till",
            field=models.DateField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
    ]
