# Generated by Django 4.2.3 on 2023-07-22 21:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0028_ratesource_ratearea_rate_area_rate_source"),
        ("project_planning", "0026_sourcebearerentitytype_karmagat"),
        ("plan_execution", "0018_institutionalcollaborationmandate_project"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectReportFinishedAndUpdate",
            fields=[
                (
                    "projectexecution_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="plan_execution.projectexecution",
                    ),
                ),
                ("quantity", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "expense_investment",
                    models.CharField(
                        blank=True, help_text="लगत ईष्टिमेट ", max_length=100, null=True
                    ),
                ),
                (
                    "bid_calling_date",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "bid_calling_date_eng",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "bid_enter_date",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "bid_enter_date_eng",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "karyadesh_date",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "karyadesh_date_eng",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "bid_enter_number",
                    models.IntegerField(
                        blank=True, help_text="बोलपत्रको दाखिला संख्या:", null=True
                    ),
                ),
                (
                    "published_date",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "published_date_eng",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "anticipated_completion_date",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "anticipated_completion_date_eng",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "agreement_date",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "agreement_date_eng",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "expense_investment_variation",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "variation_ru",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "variation_percent",
                    models.CharField(blank=True, max_length=3, null=True),
                ),
                (
                    "variation_for_approval",
                    models.CharField(
                        blank=True,
                        help_text="संसोधित लागत (रू.)",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "ammended_expense",
                    models.CharField(
                        blank=True,
                        help_text="संसोधित लागत (रू.)",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "advanced",
                    models.CharField(
                        blank=True, help_text="पेश्की", max_length=100, null=True
                    ),
                ),
                (
                    "paid",
                    models.CharField(
                        blank=True,
                        help_text="भुक्तानी (पेश्की फछ्र्यौट)",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "blocked_amount",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "payment_remained",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "finished_date",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "finished_date_eng",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("road_length", models.CharField(blank=True, max_length=50, null=True)),
                ("road_width", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "channel_length",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "channel_depth",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "drinking_water_pipe_length",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "kalvert_length",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "kalvert_width",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "building_length",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "building_width",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("area", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "total_storey",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("wall_length", models.CharField(blank=True, max_length=50, null=True)),
                ("wall_height", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "source_preservation_area",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "consumer_committee_name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.consumercommittee",
                    ),
                ),
                (
                    "firm_name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.organization",
                    ),
                ),
                (
                    "news_paper",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.newspaper",
                    ),
                ),
                (
                    "unit_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="prf_unit_type",
                        to="project.unit",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("plan_execution.projectexecution",),
        ),
    ]
