# Generated by Django 4.2.1 on 2024-01-05 08:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_settings", "0007_alter_booleanappsetting_setting_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appsettingcollection",
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
