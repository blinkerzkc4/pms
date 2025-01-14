# Generated by Django 4.2.1 on 2024-06-01 12:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("norm", "0027_norm_item_description_eng_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="norm",
            name="part_activity_no",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="norm",
            name="part_specification_no",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="norm",
            name="subpart_activity_no",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="norm",
            name="subpart_specification_no",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
