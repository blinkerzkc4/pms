# Generated by Django 4.2.1 on 2024-01-17 02:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0064_update_federal_models"),
        ("base_model", "0016_address_code_contactdetail_code_contactperson_code"),
        ("plan_execution", "0124_update_installment_model_again"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("budget_process", "0025_approveprocess_code_budgetammendment_code_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BudgetImportLog",
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
                    "code",
                    models.CharField(
                        blank=True,
                        help_text="कोड",
                        max_length=55,
                        null=True,
                        verbose_name="Code",
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
                ("imported_file", models.FileField(upload_to="budget_import_logs")),
                ("import_payload", models.JSONField()),
                ("import_status", models.BooleanField(default=False)),
                ("status", models.BooleanField(blank=True, default=True, null=True)),
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
                    "imported_addresses",
                    models.ManyToManyField(
                        blank=True, related_name="import_log", to="base_model.address"
                    ),
                ),
                (
                    "imported_bem",
                    models.ManyToManyField(
                        blank=True,
                        related_name="import_log",
                        to="budget_process.budgetexpensemanagement",
                    ),
                ),
                (
                    "imported_budget_allocation_details",
                    models.ManyToManyField(
                        blank=True,
                        related_name="import_log",
                        to="plan_execution.budgetallocationdetail",
                    ),
                ),
                (
                    "imported_project_executions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="import_log",
                        to="plan_execution.projectexecution",
                    ),
                ),
                (
                    "imported_projects",
                    models.ManyToManyField(
                        blank=True, related_name="import_log", to="project.project"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
