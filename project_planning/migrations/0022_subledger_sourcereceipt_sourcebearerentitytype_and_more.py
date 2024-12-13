# Generated by Django 4.2.1 on 2023-06-15 17:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0017_quantity"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project_planning", "0021_projectstartdecision_newspaper_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubLedger",
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
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("status", models.BooleanField(default=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
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
            name="SourceReceipt",
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
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("status", models.BooleanField(default=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
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
            name="SourceBearerEntityType",
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
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("status", models.BooleanField(default=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
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
            name="SourceBearerEntity",
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
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("status", models.BooleanField(default=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "bearer_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.sourcebearerentitytype",
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
                    "organization_name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.organization",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PaymentMethod",
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
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("status", models.BooleanField(default=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
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
            name="Module",
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
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("status", models.BooleanField(default=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
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
            name="CollectPayment",
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
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("status", models.BooleanField(default=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
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
            name="BudgetSubTitle",
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
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("status", models.BooleanField(default=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
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
            name="BudgetSource",
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
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("status", models.BooleanField(default=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("email", models.CharField(blank=True, max_length=120, null=True)),
                ("country", models.CharField(blank=True, max_length=20, null=True)),
                ("address", models.CharField(blank=True, max_length=220, null=True)),
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
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.budgetsource",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="AccountTitleManagement",
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
                ("code", models.CharField(blank=True, max_length=55, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("name_eng", models.CharField(blank=True, max_length=100, null=True)),
                ("status", models.BooleanField(default=True)),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "optional_code",
                    models.CharField(blank=True, max_length=55, null=True),
                ),
                (
                    "display_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "display_name_eng",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("is_budgeted", models.BooleanField(default=False)),
                ("sapati", models.BooleanField(default=False)),
                ("transfer_account", models.BooleanField(default=False)),
                ("fund_account", models.BooleanField(default=False)),
                (
                    "current_capital",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("हालको", "हालको"),
                            ("पुँजीगत", "पुँजीगत"),
                            ("दुवै", "दुवै"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "current_ratio",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "capital_ratio",
                    models.CharField(blank=True, max_length=255, null=True),
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
                    "module",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="atm_module",
                        to="project_planning.submodule",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project_planning.accounttitlemanagement",
                    ),
                ),
                (
                    "sub_module",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="atm_submodule",
                        to="project_planning.submodule",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
