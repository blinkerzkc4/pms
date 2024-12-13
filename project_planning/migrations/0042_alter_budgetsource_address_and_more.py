# Generated by Django 4.2.1 on 2023-11-26 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0041_alter_accounttitlemanagement_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budgetsource",
            name="address",
            field=models.CharField(
                blank=True,
                help_text="ठेगाना",
                max_length=220,
                null=True,
                verbose_name="Address",
            ),
        ),
        migrations.AlterField(
            model_name="budgetsource",
            name="country",
            field=models.CharField(
                blank=True,
                help_text="देश",
                max_length=20,
                null=True,
                verbose_name="Country",
            ),
        ),
        migrations.AlterField(
            model_name="budgetsource",
            name="email",
            field=models.CharField(
                blank=True,
                help_text="इमेल",
                max_length=120,
                null=True,
                verbose_name="Email",
            ),
        ),
        migrations.AlterField(
            model_name="budgetsource",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                help_text="अभिभावक बजेट स्रोत",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project_planning.budgetsource",
                verbose_name="Parent Budget Source",
            ),
        ),
        migrations.AlterField(
            model_name="budgetsource",
            name="phone_number",
            field=models.CharField(
                blank=True,
                help_text="फोन नं.",
                max_length=20,
                null=True,
                verbose_name="Phone Number",
            ),
        ),
        migrations.AlterField(
            model_name="budgetsource",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
    ]