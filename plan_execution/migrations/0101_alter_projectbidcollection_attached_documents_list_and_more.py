# Generated by Django 4.2.1 on 2023-12-27 05:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0100_alter_projectexecution_work_proposer_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectbidcollection",
            name="attached_documents_list",
            field=models.CharField(blank=True, max_length=155255, null=True),
        ),
        migrations.AlterField(
            model_name="projectbidcollection",
            name="bail_amount",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="projectbidcollection",
            name="bank_guarantee_no",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="projectbidcollection",
            name="total",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="projectbidcollection",
            name="total_amount",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]