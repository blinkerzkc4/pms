# Generated by Django 4.2.1 on 2023-06-07 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base_model", "0002_contactperson_contactdetail"),
    ]

    operations = [
        migrations.RenameField(
            model_name="address",
            old_name="toll",
            new_name="tole",
        ),
        migrations.RenameField(
            model_name="address",
            old_name="toll_eng",
            new_name="tole_eng",
        ),
        migrations.AddField(
            model_name="gender",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterModelTable(
            name="gender",
            table=None,
        ),
    ]