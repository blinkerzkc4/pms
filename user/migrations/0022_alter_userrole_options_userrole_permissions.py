# Generated by Django 4.2.1 on 2023-10-15 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("user", "0021_user_status_userrole_status_alter_client_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userrole",
            options={"ordering": ("municipality", "title")},
        ),
        migrations.AddField(
            model_name="userrole",
            name="permissions",
            field=models.ManyToManyField(
                related_name="granted_roles", to="auth.permission"
            ),
        ),
    ]
