# Generated by Django 4.2.1 on 2023-08-09 15:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_report', '0006_remove_templatefieldmapping_client_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='templatefieldmapping',
            name='client_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_user', to=settings.AUTH_USER_MODEL),
        ),
    ]