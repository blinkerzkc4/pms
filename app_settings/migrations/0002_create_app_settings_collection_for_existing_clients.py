from django.db import migrations, models


def create_app_settings_collection_for_existing_clients(apps, schema_editor):
    AppSettingCollection = apps.get_model("app_settings", "AppSettingCollection")
    Client = apps.get_model("user", "Client")
    db_alias = schema_editor.connection.alias
    for client in Client.objects.using(db_alias).all():
        AppSettingCollection.objects.using(db_alias).create(
            municipality=client.municipality
        )


class Migration(migrations.Migration):
    dependencies = [
        ("app_settings", "0001_initial"),
        ("user", "0031_alter_client_created_by_alter_client_created_date_and_more"),
    ]

    operations = [
        migrations.RunPython(
            create_app_settings_collection_for_existing_clients,
            migrations.RunPython.noop,
        )
    ]
