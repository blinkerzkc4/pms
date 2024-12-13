# Generated by Django 4.2.1 on 2023-08-10 13:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan_execution', '0026_projecttask'),
        ('project_report', '0007_templatefieldmapping_client_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatefieldmapping',
            name='pms_process_id',
            field=models.ForeignKey(blank=True, help_text='सञ्चालन प्रकृया', null=True, on_delete=django.db.models.deletion.SET_NULL, to='plan_execution.startpmsprocess'),
        ),
    ]