# Generated by Django 4.2.1 on 2024-01-05 08:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base_model", "0015_address_village_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=55,
                null=True,
                verbose_name="Code",
            ),
        ),
        migrations.AddField(
            model_name="contactdetail",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=55,
                null=True,
                verbose_name="Code",
            ),
        ),
        migrations.AddField(
            model_name="contactperson",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=55,
                null=True,
                verbose_name="Code",
            ),
        ),
    ]