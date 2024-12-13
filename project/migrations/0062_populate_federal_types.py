from django.db import migrations

from utils.import_csv_data import get_federal_types_from_csv
from utils.search import search_list_of_dicts


def populate_federal_types(apps, schema_editor):
    FederalType = apps.get_model("project", "FederalType")
    federal_types = get_federal_types_from_csv()
    db_alias = schema_editor.connection.alias
    for federal_type in federal_types:
        copied_federal_type = federal_type.copy()
        upper_level_type_id = copied_federal_type.pop("upper_level_type_id")
        federal_type_id = copied_federal_type.pop("id")
        if upper_level_type_id:
            parent_federal_type = search_list_of_dicts(
                federal_types, "id", upper_level_type_id
            )
            copied_parent_federal_type = parent_federal_type.copy()
            copied_parent_federal_type.pop("upper_level_type_id")
            copied_parent_federal_type.pop("id")
            (
                parent_federal_type_model,
                parent_federal_type_model_created,
            ) = FederalType.objects.using(db_alias).get_or_create(
                **copied_parent_federal_type
            )
            copied_federal_type["upper_federal_type"] = parent_federal_type_model
        (
            federal_type_model,
            federal_type_model_created,
        ) = FederalType.objects.using(
            db_alias
        ).get_or_create(**copied_federal_type)


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0061_districtratefiles_code_estimate_code_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_federal_types),
    ]
