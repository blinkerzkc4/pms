# Generated by Django 4.2.1 on 2024-01-19 09:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0039_client_code_userrole_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="database_host",
            field=models.GenericIPAddressField(default="172.19.0.24", protocol="IPv4"),
        ),
        migrations.AddField(
            model_name="client",
            name="database_name",
            field=models.CharField(default="yojana_db", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="client",
            name="database_password",
            field=models.CharField(default="Yoj@na@321", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="client",
            name="database_port",
            field=models.CharField(default="5432", max_length=4),
        ),
        migrations.AddField(
            model_name="client",
            name="database_user",
            field=models.CharField(default="yojana_db_user", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="client",
            name="subdomain",
            field=models.CharField(default="yojana.lgerp.org", max_length=255),
        ),
    ]
