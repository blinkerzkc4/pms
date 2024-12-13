# Generated by Django 4.2.1 on 2023-05-16 15:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0003_auto_20230514_0846"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="muncipality",
            options={"verbose_name_plural": "Muncipalities"},
        ),
        migrations.AddField(
            model_name="rate",
            name="muncipality",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.muncipality",
            ),
        ),
        migrations.CreateModel(
            name="DistrictRateFiles",
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
                ("title", models.CharField(blank=True, max_length=255)),
                ("file", models.FileField(upload_to="uploads/district_rates/")),
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
                    "district",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project.district",
                    ),
                ),
                (
                    "financial_year",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project.financialyear",
                    ),
                ),
                (
                    "muncipality",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="project.muncipality",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]