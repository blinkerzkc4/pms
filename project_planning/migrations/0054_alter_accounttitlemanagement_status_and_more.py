# Generated by Django 4.2.1 on 2023-12-17 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0053_consumercommitteemember_country_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accounttitlemanagement",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="bankaccount",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="office",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="organization",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="organizationmember",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="road",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="sourcebearerentity",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="standinglist",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="standinglisttype",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]