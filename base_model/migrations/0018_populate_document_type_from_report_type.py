# Generated by Django 4.2.1 on 2024-03-05 19:29

from django.db import migrations


def populate_document_type_from_report_type(apps, schema_editor):
    DocumentType = apps.get_model("base_model", "DocumentType")
    ReportType = apps.get_model("project_report", "ReportType")
    db_alias = schema_editor.connection.alias
    for report_type in ReportType.objects.using(db_alias).all():
        DocumentType.objects.using(db_alias).create(
            code=report_type.code,
            name=report_type.name,
            name_eng=report_type.name_eng,
            detail=report_type.detail,
            document_type="report_type",
        )


def reverse_document_type_from_report_type(apps, schema_editor):
    DocumentType = apps.get_model("base_model", "DocumentType")
    ReportType = apps.get_model("project_report", "ReportType")
    db_alias = schema_editor.connection.alias
    report_type_codes = ReportType.objects.using(db_alias).values_list(
        "code", flat=True
    )
    DocumentType.objects.using(db_alias).filter(code__in=report_type_codes).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("base_model", "0017_address_updated_by_contactdetail_updated_by_and_more"),
        ("project_report", "0039_populate_report_type"),
    ]

    operations = [
        migrations.RunPython(
            populate_document_type_from_report_type,
            reverse_document_type_from_report_type,
        )
    ]
