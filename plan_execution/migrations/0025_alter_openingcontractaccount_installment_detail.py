# Generated by Django 4.2.3 on 2023-07-30 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_execution", "0024_alter_projectfinishedbailreturn_project"),
    ]

    operations = [
        migrations.AlterField(
            model_name="openingcontractaccount",
            name="installment_detail",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="open_account_installment",
                to="plan_execution.installmentdetail",
            ),
        ),
    ]
