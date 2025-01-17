# Generated by Django 4.2.1 on 2024-01-04 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0054_alter_accounttitlemanagement_status_and_more"),
        (
            "plan_execution",
            "0105_alter_openingcontractaccount_secretary_of_consumer_committee_post_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="openingcontractaccount",
            name="secretary_of_consumer_committee_post",
            field=models.ForeignKey(
                blank=True,
                help_text="उपभोक्ता समिति सचिव पद",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="oca_secretary",
                to="project_planning.consumercommitteemember",
                verbose_name="Secretary of Consumer Committee Post",
            ),
        ),
        migrations.AlterField(
            model_name="openingcontractaccount",
            name="witness_consumer_committee_post",
            field=models.ForeignKey(
                blank=True,
                help_text="साक्षी उपभोक्ता समिति पद",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="oca_witness",
                to="project_planning.consumercommitteemember",
                verbose_name="Witness Consumer Committee Post",
            ),
        ),
    ]
