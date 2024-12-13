# Generated by Django 4.2.1 on 2023-12-09 03:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "plan_execution",
            "0060_consumerformulation_selected_consumer_committee_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectbidcollection",
            name="bail_type",
            field=models.CharField(
                blank=True,
                default="बैल",
                max_length=50,
                null=True,
                verbose_name=(("bank_guarantee", "बैंक ग्यारेन्टि"), ("cash", "नगद")),
            ),
        ),
        migrations.AlterField(
            model_name="projectbidcollection",
            name="bank_guarantee_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("bid_bond ", "बिड बन्ड "),
                    ("performance_bond", "पर्फरमेन्स बन्ड"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
