# Generated by Django 4.2.1 on 2023-12-10 17:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "plan_execution",
            "0062_rename_body_projectmobilizationdetail_institution_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="consumerformulation",
            name="consumer_committee_name",
            field=models.CharField(
                blank=True,
                help_text="उपभोक्ता समिति नाम",
                max_length=255,
                null=True,
                verbose_name="Consumer Committee Name",
            ),
        ),
    ]
