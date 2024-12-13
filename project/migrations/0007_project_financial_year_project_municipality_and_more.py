# Generated by Django 4.2.1 on 2023-05-22 17:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0006_estimate_estimationrate_jdcomment_jobdescription_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="financial_year",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.financialyear",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="municipality",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.municipality",
            ),
        ),
        migrations.AlterField(
            model_name="districtratefiles",
            name="municipality",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.municipality",
            ),
        ),
        migrations.AlterField(
            model_name="estimationrate",
            name="breadth",
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name="estimationrate",
            name="height",
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name="estimationrate",
            name="length",
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name="estimationrate",
            name="quantity",
            field=models.DecimalField(decimal_places=5, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name="rate",
            name="municipality",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.municipality",
            ),
        ),
        migrations.AlterField(
            model_name="topic",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.topic",
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="municipality",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.municipality",
            ),
        ),
        migrations.CreateModel(
            name="ProjectCategory",
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
                ("name", models.CharField(blank=True, max_length=120)),
                ("name_unicode", models.CharField(blank=True, max_length=120)),
                ("name_eng", models.CharField(blank=True, max_length=120)),
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
        migrations.AddField(
            model_name="project",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.projectcategory",
            ),
        ),
    ]