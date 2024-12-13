# Generated by Django 4.2.1 on 2023-12-15 06:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0053_consumercommitteemember_country_and_more"),
        ("plan_execution", "0074_alter_projectdarbhaubid_accountant_opinion_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectexecution",
            name="purpose",
            field=models.ForeignKey(
                blank=True,
                help_text="उद्देश्य",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project_planning.purposeplan",
                verbose_name="Purpose",
            ),
        ),
        migrations.AddField(
            model_name="projectexecution",
            name="work_area",
            field=models.ForeignKey(
                blank=True,
                help_text="कार्यक्षेत्र",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="wa_execution",
                to="project_planning.subjectarea",
                verbose_name="Work Area",
            ),
        ),
        migrations.AlterField(
            model_name="projectexecution",
            name="subject_area",
            field=models.ForeignKey(
                blank=True,
                help_text="विषयगत कार्यक्षेत्र",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sa_execution",
                to="project_planning.subjectarea",
                verbose_name="Subject Area",
            ),
        ),
    ]
