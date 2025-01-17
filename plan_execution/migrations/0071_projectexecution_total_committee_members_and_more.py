# Generated by Django 4.2.1 on 2023-12-15 02:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0070_commentandorder"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectexecution",
            name="total_committee_members",
            field=models.IntegerField(
                blank=True,
                help_text="जम्मा समुदाय संख्या",
                null=True,
                verbose_name="Total Committee Members",
            ),
        ),
        migrations.AddField(
            model_name="projectexecution",
            name="total_gathered_organizations",
            field=models.IntegerField(
                blank=True,
                help_text="जम्मा संगठित संस्था संख्या",
                null=True,
                verbose_name="Total Gathered Organizations",
            ),
        ),
    ]
