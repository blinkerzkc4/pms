# Generated by Django 4.2.1 on 2023-06-06 17:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base_model", "0002_contactperson_contactdetail"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project_planning", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bank",
            name="current_address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bank_crr_address",
                to="base_model.address",
            ),
        ),
        migrations.AddField(
            model_name="bank",
            name="detail",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="bank",
            name="former_address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bank_former_address",
                to="base_model.address",
            ),
        ),
        migrations.AddField(
            model_name="bank",
            name="full_name",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="bank",
            name="full_name_eng",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="bank",
            name="office",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="bank",
            name="registration_date",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="bank",
            name="registration_date_eng",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="bank",
            name="registration_no",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="bank",
            name="status",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="ChequeFormat",
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
                "db_table": "cheque_format",
            },
        ),
        migrations.CreateModel(
            name="BankType",
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
                "db_table": "bank_type",
            },
        ),
        migrations.AddField(
            model_name="bank",
            name="bank_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bank_type",
                to="project_planning.banktype",
            ),
        ),
        migrations.AddField(
            model_name="bank",
            name="cheque_format",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cheque_format",
                to="project_planning.chequeformat",
            ),
        ),
    ]
