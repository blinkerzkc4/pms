# Generated by Django 4.2.1 on 2023-10-17 05:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0022_alter_userrole_options_userrole_permissions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userrole",
            name="districtrate_create",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="districtrate_delete",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="districtrate_edit",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="ratecategory_create",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="ratecategory_delete",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="ratecategory_edit",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="role_create",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="role_deactivate",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="role_delete",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="role_detail",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="role_edit",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="unit_create",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="unit_delete",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="unit_edit",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="user_activity",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="user_add",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="user_changeactivity",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="user_deactivate",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="user_delete",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="user_details",
        ),
        migrations.RemoveField(
            model_name="userrole",
            name="user_edit",
        ),
    ]
