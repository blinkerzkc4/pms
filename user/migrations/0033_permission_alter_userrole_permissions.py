# Generated by Django 4.2.1 on 2023-12-28 06:27

import django.db.models.deletion
from django.db import migrations, models


def remove_old_permissions(apps, schema_editor):
    UserRole = apps.get_model("user", "UserRole")
    db_alias = schema_editor.connection.alias
    for user_role in UserRole.objects.using(db_alias).all():
        user_role.permissions.clear()


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0032_alter_user_status_alter_userrole_status"),
    ]

    operations = [
        migrations.RunPython(remove_old_permissions),
    ]
