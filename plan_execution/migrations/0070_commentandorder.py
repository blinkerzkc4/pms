# Generated by Django 4.2.1 on 2023-12-15 02:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "plan_execution",
            "0069_alter_probabilitystudyapprove_approvers_opinion_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="CommentAndOrder",
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
                    "cha_no",
                    models.CharField(
                        blank=True,
                        help_text="चलानी नं",
                        max_length=255,
                        null=True,
                        verbose_name="Invoice Number",
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
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plan_execution.projectexecution",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
