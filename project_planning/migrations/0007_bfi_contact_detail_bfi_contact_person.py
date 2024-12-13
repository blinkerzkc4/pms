# Generated by Django 4.2.1 on 2023-06-10 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "base_model",
            "0004_remove_address_district_remove_address_local_level_and_more",
        ),
        ("project_planning", "0006_submodule_bankaccount"),
    ]

    operations = [
        migrations.AddField(
            model_name="bfi",
            name="contact_detail",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bank_contact_detail",
                to="base_model.contactdetail",
            ),
        ),
        migrations.AddField(
            model_name="bfi",
            name="contact_person",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bank_contact_person",
                to="base_model.contactperson",
            ),
        ),
    ]
