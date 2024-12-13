# Generated by Django 4.2.1 on 2023-06-12 02:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0017_quantity"),
        ("user", "0010_user_full_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserRole",
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
                ("title", models.CharField(max_length=255)),
                ("user_add", models.BooleanField(default=False)),
                ("user_details", models.BooleanField(default=False)),
                ("user_edit", models.BooleanField(default=False)),
                ("user_delete", models.BooleanField(default=False)),
                ("user_deactivate", models.BooleanField(default=False)),
                ("user_activity", models.BooleanField(default=False)),
                ("user_changeactivity", models.BooleanField(default=False)),
                ("role_create", models.BooleanField(default=False)),
                ("role_edit", models.BooleanField(default=False)),
                ("role_detail", models.BooleanField(default=False)),
                ("role_deactivate", models.BooleanField(default=False)),
                ("role_delete", models.BooleanField(default=False)),
                ("districtrate_create", models.BooleanField(default=False)),
                ("districtrate_edit", models.BooleanField(default=False)),
                ("districtrate_delete", models.BooleanField(default=False)),
                ("ratecategory_create", models.BooleanField(default=False)),
                ("ratecategory_edit", models.BooleanField(default=False)),
                ("ratecategory_delete", models.BooleanField(default=False)),
                ("unit_create", models.BooleanField(default=False)),
                ("unit_edit", models.BooleanField(default=False)),
                ("unit_delete", models.BooleanField(default=False)),
                (
                    "municipality",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.municipality",
                    ),
                ),
            ],
            options={
                "unique_together": {("municipality", "title")},
            },
        ),
        migrations.AddField(
            model_name="user",
            name="user_role",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="user.userrole",
            ),
        ),
    ]