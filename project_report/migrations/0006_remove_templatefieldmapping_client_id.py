# Generated by Django 4.2.1 on 2023-08-09 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_report', '0005_remove_templatefieldmapping_deleted_uq_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templatefieldmapping',
            name='client_id',
        ),
    ]