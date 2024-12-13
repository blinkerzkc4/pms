# Generated by Django 4.2.1 on 2023-12-14 10:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0068_paymentexitbill_nikasha_total_amount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="probabilitystudyapprove",
            name="approvers_opinion",
            field=models.TextField(
                blank=True,
                default="",
                help_text="अनुमोदनको अभिप्राय",
                verbose_name="Approver's Opinion",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="probabilitystudyapprove",
            name="consumer_benefits",
            field=models.TextField(
                blank=True,
                default="",
                help_text="उपभोक्ता लाभ",
                verbose_name="Consumer Benefits",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="probabilitystudyapprove",
            name="decision",
            field=models.TextField(
                blank=True, default="", help_text="निर्णय", verbose_name="Decision"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="probabilitystudyapprove",
            name="engineer_survey_to_start_future",
            field=models.TextField(
                blank=True,
                default="",
                help_text="अभियन्ता सर्वेक्षण भविष्यमा सुरु गर्ने",
                verbose_name="Engineer Survey To Start Future",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="probabilitystudyapprove",
            name="label",
            field=models.TextField(
                blank=True,
                help_text="लेबल",
                max_length=255,
                null=True,
                verbose_name="Label",
            ),
        ),
        migrations.AlterField(
            model_name="probabilitystudyapprove",
            name="recommender_opinion",
            field=models.TextField(
                blank=True,
                default="",
                help_text="सिफारिसको अभिप्राय",
                verbose_name="Recommender's Opinion",
            ),
            preserve_default=False,
        ),
    ]