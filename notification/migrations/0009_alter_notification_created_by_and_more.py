# Generated by Django 4.2.1 on 2024-03-25 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("plan_execution", "0132_rename_document_usercommitteedocuments_document_file"),
        ("notification", "0008_notification_updated_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="official_process",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="plan_execution.officialprocess",
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="plan_execution.projectexecution",
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updated By",
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="notification_for",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
