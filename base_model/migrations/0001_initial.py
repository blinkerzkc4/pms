# Generated by Django 4.2.1 on 2023-06-06 16:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("project", "0012_ratecategory_rate_category"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Gender",
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
                "db_table": "gender",
            },
        ),
        migrations.CreateModel(
            name="Address",
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
                ("house_no", models.CharField(blank=True, max_length=55, null=True)),
                ("toll", models.CharField(blank=True, max_length=55, null=True)),
                ("toll_eng", models.CharField(blank=True, max_length=55, null=True)),
                ("road_name", models.CharField(blank=True, max_length=55, null=True)),
                (
                    "road_name_eng",
                    models.CharField(blank=True, max_length=55, null=True),
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
                    "district",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="district_address",
                        to="project.district",
                    ),
                ),
                (
                    "local_level",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="municipality_address",
                        to="project.municipality",
                    ),
                ),
                (
                    "provence",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="province_address",
                        to="project.province",
                    ),
                ),
                (
                    "ward_no",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="ward_address",
                        to="project.ward",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]