# Generated by Django 4.2.1 on 2023-06-17 16:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project_planning", "0024_alter_sourcebearerentity_bearer_type"),
        ("project", "0019_alter_quantity_options"),
        (
            "budget_process",
            "0004_rename_income_title_incomebudgetrangedetermine_parent",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="BudgetExpenseManagement",
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
                (
                    "expense_title_number",
                    models.CharField(blank=True, max_length=55, null=True),
                ),
                ("first_quarter", models.IntegerField(blank=True, null=True)),
                ("second_quarter", models.IntegerField(blank=True, null=True)),
                ("third_quarter", models.IntegerField(blank=True, null=True)),
                ("forth_quarter", models.IntegerField(blank=True, null=True)),
                (
                    "estimated_expense_amount",
                    models.IntegerField(blank=True, null=True),
                ),
                ("status", models.BooleanField(default=False)),
                (
                    "activity_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("aim", models.IntegerField(blank=True, null=True)),
                ("unit", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "approval_process",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="budget_process.approveprocess",
                    ),
                ),
                (
                    "budget_source",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.budgetsource",
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
                    "financial_year",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project.financialyear",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        help_text="shirshak ko name",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="budget_process.budgetexpensemanagement",
                    ),
                ),
                (
                    "sub_module",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.submodule",
                    ),
                ),
                (
                    "subject_area",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.subjectarea",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
