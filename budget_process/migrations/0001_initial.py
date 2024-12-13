# Generated by Django 4.2.1 on 2023-06-17 06:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("employee", "0007_cumulativedetail_cif_certificate_no"),
        ("project", "0019_alter_quantity_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApproveProcess",
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
                ("status", models.BooleanField(default=True)),
                (
                    "prepared_date",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "prepared_date_eng",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "verified_date",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "verified_date_eng",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "approved_date",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "approved_date_eng",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "approved_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="a_employee",
                        to="employee.employee",
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
                    "prepared_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="p_employee",
                        to="employee.employee",
                    ),
                ),
                (
                    "verified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="v_employee",
                        to="employee.employee",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Source",
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
                ("status", models.BooleanField(default=True)),
                ("internal_source", models.IntegerField(blank=True, null=True)),
                ("nepal_gov", models.IntegerField(blank=True, null=True)),
                ("province_gov", models.IntegerField(blank=True, null=True)),
                ("local_gov", models.IntegerField(blank=True, null=True)),
                ("loan", models.IntegerField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="IncomeBudgetRangeDetermine",
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
                ("status", models.BooleanField(default=True)),
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
                ("estimated_amount", models.IntegerField(blank=True, null=True)),
                ("date", models.CharField(blank=True, max_length=100, null=True)),
                ("date_eng", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "income_title_no",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "approve_process",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="approve_process_ibrd",
                        to="budget_process.approveprocess",
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
                    "income_title",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="budget_process.incomebudgetrangedetermine",
                    ),
                ),
                (
                    "source_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="budget_process.source",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ExpenseBudgetRangeDetermine",
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
                ("status", models.BooleanField(default=True)),
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
                ("estimated_amount", models.IntegerField(blank=True, null=True)),
                ("date", models.CharField(blank=True, max_length=100, null=True)),
                ("date_eng", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "expense_determine_level",
                    models.CharField(
                        choices=[
                            ("ward", "Ward"),
                            ("other", "Other"),
                            ("municipality", "Municipality"),
                        ],
                        max_length=15,
                    ),
                ),
                ("ward", models.IntegerField(blank=True, null=True)),
                (
                    "expense_title_no",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "approve_process",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="approve_process_ebrd",
                        to="budget_process.approveprocess",
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
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="budget_process.expensebudgetrangedetermine",
                    ),
                ),
                (
                    "source_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="budget_process.source",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EstimateFinancialArrangements",
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
                ("status", models.BooleanField(default=True)),
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
                ("estimated_amount", models.IntegerField(blank=True, null=True)),
                ("date", models.CharField(blank=True, max_length=100, null=True)),
                ("date_eng", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "income_title_no",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "approve_process",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="approve_process_efa",
                        to="budget_process.approveprocess",
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
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="budget_process.estimatefinancialarrangements",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]