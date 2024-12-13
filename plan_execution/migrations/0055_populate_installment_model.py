from django.db import migrations


def populate_installment_model(apps, schema_editor):
    Installment = apps.get_model("plan_execution", "ProjectInstallment")
    installment_data_list = [
        {
            "code": "first",
            "name": "पहिलो किस्ता",
            "name_eng": "First Installment",
        },
        {
            "code": "second",
            "name": "दोस्रो किस्ता",
            "name_eng": "Second Installment",
        },
        {
            "code": "third",
            "name": "तेस्रो किस्ता",
            "name_eng": "Third Installment",
        },
        {
            "code": "fourth",
            "name": "चौथो किस्ता",
            "name_eng": "Fourth Installment",
        },
        {
            "code": "last",
            "name": "अन्तिम किस्ता",
            "name_eng": "Last Installment",
        },
    ]
    db_alias = schema_editor.connection.alias
    Installment.objects.using(db_alias).bulk_create(
        Installment(**data) for data in installment_data_list
    )


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0054_alter_installmentdetail_installment_and_more"),
    ]

    operations = [
        migrations.RunPython(
            populate_installment_model, reverse_code=migrations.RunPython.noop
        ),
    ]
