# Generated by Django 4.1 on 2023-09-02 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_execution", "0030_projectexecutiondocument_doc_size_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectphysicaldescription",
            name="remarks",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="projectphysicaldescription",
            name="unit",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]