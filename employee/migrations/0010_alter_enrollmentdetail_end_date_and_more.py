# Generated by Django 4.2.1 on 2023-07-16 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0009_alter_enrollmentdetail_end_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="enrollmentdetail",
            name="end_date",
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name="enrollmentdetail",
            name="start_date",
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
