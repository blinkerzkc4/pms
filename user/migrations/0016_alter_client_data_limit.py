# Generated by Django 4.2.1 on 2023-10-02 17:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0015_alter_client_main_admin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="data_limit",
            field=models.PositiveIntegerField(default=512),
        ),
    ]
