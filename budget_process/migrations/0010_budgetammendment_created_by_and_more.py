# Generated by Django 4.2.3 on 2023-07-23 09:58

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import budget_process.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("budget_process", "0009_budgetammendment_budget_management"),
    ]

    operations = [
        migrations.AddField(
            model_name="budgetammendment",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="budgetammendment",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="budgetammendment",
            name="updated_date",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="budgetammendment",
            name="budget_management",
            field=models.IntegerField(
                blank=True,
                help_text="बजेट व्यवस्थापन:",
                null=True,
                verbose_name=budget_process.models.BudgetManagement,
            ),
        ),
        migrations.AlterField(
            model_name="budgetammendment",
            name="kramagat",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="budgetammendment",
            name="status",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="estimatefinancialarrangements",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="expensebudgetrangedetermine",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="incomebudgetrangedetermine",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.CreateModel(
            name="BudgetManagement",
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
                ("acc_id", models.IntegerField(blank=True, null=True)),
                ("value", models.IntegerField(blank=True, null=True)),
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
    ]