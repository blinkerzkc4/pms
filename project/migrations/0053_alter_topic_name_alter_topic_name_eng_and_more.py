# Generated by Django 4.2.1 on 2023-11-01 10:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0052_alter_rate_title_alter_rate_title_eng"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
            name="name",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="topic",
            name="name_eng",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="topic",
            name="name_unicode",
            field=models.TextField(blank=True),
        ),
    ]
