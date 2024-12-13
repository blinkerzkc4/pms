from django.db import migrations, models


def populate_gender_table(apps, schema_editor):
    Gender = apps.get_model("base_model", "Gender")
    db_alias = schema_editor.connection.alias
    Gender.objects.using(db_alias).create(code="male", name="पुरुष", name_eng="Male")
    Gender.objects.using(db_alias).create(
        code="female", name="महिला", name_eng="Female"
    )
    Gender.objects.using(db_alias).create(code="others", name="अरू", name_eng="Others")


class Migration(migrations.Migration):
    dependencies = [
        (
            "base_model",
            "0012_alter_address_created_by_alter_address_created_date_and_more",
        ),
    ]

    operations = [migrations.RunPython(populate_gender_table)]
