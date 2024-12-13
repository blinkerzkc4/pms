import django.db.models.deletion
from django.db import migrations, models


def remove_existing_executiveagency_updates(apps, schema_editor):
    ExecutiveAgency = apps.get_model("project_planning", "ExecutiveAgency")
    db_alias = schema_editor.connection.alias
    ExecutiveAgency.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("base_model", "0013_populate_gender_table"),
        (
            "project_planning",
            "0043_alter_projecttype_parent_alter_subjectarea_parent",
        ),
    ]

    operations = [
        migrations.RunPython(remove_existing_executiveagency_updates),
    ]
