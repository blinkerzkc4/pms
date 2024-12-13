# Generated by Django 4.1 on 2023-08-23 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("plan_execution", "0027_projectexecution_project"),
    ]

    operations = [
        migrations.CreateModel(
            name="OfficialProcess",
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
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("remarks", models.TextField(blank=True, null=True)),
                ("file", models.FileField(blank=True, null=True, upload_to="uploads/")),
                (
                    "send_for",
                    models.CharField(
                        choices=[
                            ("P", "Preparation"),
                            ("V", "Verification"),
                            ("A", "Approval"),
                        ],
                        default="P",
                        max_length=1,
                    ),
                ),
                ("feedback_remarks", models.TextField(blank=True, null=True)),
                (
                    "feedback_file",
                    models.FileField(blank=True, null=True, upload_to="uploads/"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("A", "Accept"), ("R", "Reject"), ("P", "Pending")],
                        default="P",
                        max_length=1,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
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
                (
                    "request_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="request_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "send_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="action_taken_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]