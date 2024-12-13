# Generated by Django 4.2.1 on 2023-06-07 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "project_planning",
            "0002_bank_current_address_bank_detail_bank_former_address_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="banktype",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="chequeformat",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="paymentmedium",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="subjectarea",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterModelTable(
            name="banktype",
            table=None,
        ),
        migrations.AlterModelTable(
            name="chequeformat",
            table=None,
        ),
        migrations.AlterModelTable(
            name="paymentmedium",
            table=None,
        ),
        migrations.AlterModelTable(
            name="subjectarea",
            table=None,
        ),
    ]
