# Generated by Django 4.2.1 on 2023-10-11 18:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employee", "0014_positionlevel_short_form"),
    ]

    operations = [
        migrations.AlterField(
            model_name="country",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="cumulativedetail",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="currentworkingdetail",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="department",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="departmentbranch",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="employeesector",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="employeetype",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="enrollmentdetail",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="familydetail",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="language",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="maritalstatus",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="nationality",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="position",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="positionlevel",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="publicrepresentativedetail",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="publicrepresentativeposition",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="religion",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="servicegroup",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="taxpayer",
            name="status",
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
