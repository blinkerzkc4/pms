# Generated by Django 4.2.1 on 2023-06-13 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0006_alter_employee_permanent_address_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cumulativedetail",
            name="cif_certificate_no",
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
