# Generated by Django 4.2.1 on 2024-01-09 05:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0116_rename_payment_type_paymentexitbill_payment_mode"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectdeadline",
            name="site_inspection_date",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
