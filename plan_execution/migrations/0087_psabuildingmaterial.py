# Generated by Django 4.2.1 on 2023-12-19 02:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0054_alter_accounttitlemanagement_status_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "plan_execution",
            "0086_openingcontractaccount_cost_participation_subsidy_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PSABuildingMaterial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="निर्माण मिति",
                        verbose_name="Created Date",
                    ),
                ),
                (
                    "updated_date",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="अद्यावधिक मिति",
                        verbose_name="Updated Date",
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=True, help_text="स्थिति", verbose_name="Status"
                    ),
                ),
                (
                    "amount",
                    models.CharField(
                        blank=True,
                        help_text="परिमाण",
                        max_length=255,
                        null=True,
                        verbose_name="Amount",
                    ),
                ),
                (
                    "rupees",
                    models.CharField(
                        blank=True,
                        help_text="रुपैयाँ",
                        max_length=255,
                        null=True,
                        verbose_name="Rupees",
                    ),
                ),
                (
                    "remark",
                    models.CharField(
                        blank=True,
                        help_text="कैफियत",
                        max_length=255,
                        null=True,
                        verbose_name="Remark",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="निर्माण गर्ने",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "material",
                    models.ForeignKey(
                        blank=True,
                        help_text="सामग्री",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.constructionmaterialdescription",
                        verbose_name="Material",
                    ),
                ),
                (
                    "probability_study_approve",
                    models.ForeignKey(
                        blank=True,
                        help_text="सम्भाव्यता अध्ययन/स्वीकृत",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="materials",
                        to="plan_execution.probabilitystudyapprove",
                        verbose_name="Probability Study Approve",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
