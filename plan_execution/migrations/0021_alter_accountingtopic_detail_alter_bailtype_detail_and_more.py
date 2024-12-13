# Generated by Django 4.2.3 on 2023-07-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan_execution", "0020_projectreportfinishedandupdate_karmagat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accountingtopic",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="bailtype",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="installment",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="planstartdecision",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="projectphysicaldescription",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="startpmsprocess",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="tenderpurchasebranch",
            name="detail",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
