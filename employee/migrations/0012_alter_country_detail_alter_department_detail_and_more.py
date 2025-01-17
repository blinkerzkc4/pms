# Generated by Django 4.2.3 on 2023-07-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0011_alter_taxpayer_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="country",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="department",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="departmentbranch",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="employeesector",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="employeetype",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="language",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="maritalstatus",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="nationality",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="position",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="positionlevel",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="publicrepresentativeposition",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="religion",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="servicegroup",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
