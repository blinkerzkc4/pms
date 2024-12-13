from django.db import migrations, models


def populate_marital_status_table(apps, schema_editor):
    MaritalStatus = apps.get_model("employee", "MaritalStatus")
    db_alias = schema_editor.connection.alias
    MaritalStatus.objects.using(db_alias).create(
        code="single", name="एकल", name_eng="Single"
    )
    MaritalStatus.objects.using(db_alias).create(
        code="married", name="विवाहित", name_eng="Married"
    )
    MaritalStatus.objects.using(db_alias).create(
        code="unmarried", name="अविवाहित", name_eng="Unmarried"
    )
    MaritalStatus.objects.using(db_alias).create(
        code="divorced", name="सम्बन्धविच्छेद", name_eng="Divorced"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("employee", "0016_alter_country_code_alter_country_created_by_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_marital_status_table),
    ]
