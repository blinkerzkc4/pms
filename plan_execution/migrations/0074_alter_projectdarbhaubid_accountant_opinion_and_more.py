# Generated by Django 4.2.1 on 2023-12-15 04:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0073_alter_projecttender_address1_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectdarbhaubid",
            name="accountant_opinion",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="projectdarbhaubid",
            name="executive_decision",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="projectdarbhaubid",
            name="office_head_decision",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="projectdarbhaubid",
            name="project_head_opinion",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="projectdarbhaubid",
            name="proprietor_name",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="projectdarbhaubid",
            name="submitter_opinion",
            field=models.TextField(blank=True, null=True),
        ),
    ]
