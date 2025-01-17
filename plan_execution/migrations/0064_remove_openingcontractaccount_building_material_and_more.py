# Generated by Django 4.2.1 on 2023-12-10 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0063_consumerformulation_consumer_committee_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="openingcontractaccount",
            name="building_material",
        ),
        migrations.RemoveField(
            model_name="openingcontractaccount",
            name="installment_detail",
        ),
        migrations.RemoveField(
            model_name="openingcontractaccount",
            name="maintenance_arrangement",
        ),
        migrations.AddField(
            model_name="buildingmaterialdetail",
            name="opening_contract_account",
            field=models.ForeignKey(
                blank=True,
                help_text="सम्झौता खाता खोलिदिने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="materials",
                to="plan_execution.openingcontractaccount",
                verbose_name="Opening Contract Account",
            ),
        ),
        migrations.AddField(
            model_name="installmentdetail",
            name="opening_contract_account",
            field=models.ForeignKey(
                blank=True,
                help_text="सम्झौता खाता खोलिदिने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="installment",
                to="plan_execution.openingcontractaccount",
                verbose_name="Opening Contract Account",
            ),
        ),
        migrations.AddField(
            model_name="maintenancearrangement",
            name="opening_contract_account",
            field=models.ForeignKey(
                blank=True,
                help_text="सम्झौता खाता खोलिदिने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="maintenance",
                to="plan_execution.openingcontractaccount",
                verbose_name="Opening Contract Account",
            ),
        ),
    ]
