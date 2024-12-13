import csv

from django.db import migrations, models

from project_report.models import ReportType as ReportTypeModel
from project_report.models import TemplateFieldMapping as TemplateFieldMappingModel
from project_report.models import (
    TemplateFieldMappingGroup as TemplateFieldMappingGroupModel,
)


def get_field_mapping_model(apps) -> TemplateFieldMappingModel:
    return apps.get_model("project_report", "TemplateFieldMapping")


def populate_deposit_field_mappings(apps, schema_editor):
    TemplateFieldMapping = get_field_mapping_model(apps)
    TemplateFieldMappingGroup: TemplateFieldMappingGroupModel = apps.get_model(
        "project_report", "TemplateFieldMappingGroup"
    )
    StartPmsProcess = apps.get_model("plan_execution", "StartPmsProcess")
    db_alias = schema_editor.connection.alias
    deposit_mandate_field_mappings_group = (
        TemplateFieldMappingGroup.objects.using(db_alias)
        .filter(code="deposit_mandate")
        .first()
    )
    deposit_mandate_process = (
        StartPmsProcess.objects.using(db_alias).filter(code="dp").first()
    )

    with open(
        "project_report/data/deposit_mandate_field_mappings.csv",
        "r",
        encoding="utf-8-sig",
    ) as deposit_mandate_field_mappings:
        reader = csv.DictReader(deposit_mandate_field_mappings)
        for row in reader:
            TemplateFieldMapping.objects.using(db_alias).create(
                code=row["code"],
                name=row["name nepali"],
                name_eng=row["name"],
                pms_process_id=deposit_mandate_process,
                group=deposit_mandate_field_mappings_group,
            )


def populate_quot_spec_mappings(apps, schema_editor):
    TemplateFieldMapping = get_field_mapping_model(apps)
    db_alias = schema_editor.connection.alias
    TemplateFieldMappingGroup: TemplateFieldMappingGroupModel = apps.get_model(
        "project_report", "TemplateFieldMappingGroup"
    )
    StartPmsProcess = apps.get_model("plan_execution", "StartPmsProcess")
    quot_spec_field_mappings_group = TemplateFieldMappingGroup.objects.using(
        db_alias
    ).create(
        code="quot_spec",
        name_eng="Quotation Specification",
        name="उद्धरण विवरण",
    )
    quot_spec_process = (
        StartPmsProcess.objects.using(db_alias).filter(code="quot").first()
    )

    with open(
        "project_report/data/quot_spec_field_mapping_data.csv",
        "r",
        encoding="utf-8-sig",
    ) as deposit_mandate_field_mappings:
        reader = csv.DictReader(deposit_mandate_field_mappings)
        for row in reader:
            TemplateFieldMapping.objects.using(db_alias).create(
                code=row["code"],
                name=row["name nepali"],
                name_eng=row["name"],
                pms_process_id=quot_spec_process,
                group=quot_spec_field_mappings_group,
            )


def populate_quot_sa_mappings(apps, schema_editor):
    TemplateFieldMapping = get_field_mapping_model(apps)
    TemplateFieldMappingGroup: TemplateFieldMappingGroupModel = apps.get_model(
        "project_report", "TemplateFieldMappingGroup"
    )
    db_alias = schema_editor.connection.alias
    StartPmsProcess = apps.get_model("plan_execution", "StartPmsProcess")
    quot_spec_field_mappings_group = TemplateFieldMappingGroup.objects.using(
        db_alias
    ).create(
        code="quot_sa",
        name_eng="Quotation Submission Approval",
        name="उद्धरण पेशगर्ने अनुमोदन",
    )
    quot_spec_process = (
        StartPmsProcess.objects.using(db_alias).filter(code="quot").first()
    )

    with open(
        "project_report/data/quot_sa_field_mapping_data.csv",
        "r",
        encoding="utf-8-sig",
    ) as deposit_mandate_field_mappings:
        reader = csv.DictReader(deposit_mandate_field_mappings)
        for row in reader:
            TemplateFieldMapping.objects.using(db_alias).create(
                code=row["code"],
                name=row["name nepali"],
                name_eng=row["name"],
                pms_process_id=quot_spec_process,
                group=quot_spec_field_mappings_group,
            )


def populate_report_types(apps, schema_editor):
    ReportType: ReportTypeModel = apps.get_model("project_report", "ReportType")
    report_types = [
        {
            "code": "quotation_specification_report",
            "name_np": "उद्धरण विवरण रिपोर्ट",
            "text": "Quotation Specification Report",
        },
        {
            "code": "estimate_submit_report",
            "name_np": "अनुमान सबमिट रिपोर्ट",
            "text": "Estimate Submit Report",
        },
        {
            "code": "invitation_for_proposal_reports",
            "name_np": "प्रस्ताव आमन्त्रण रिपोर्ट",
            "text": "Invitation For Proposal Report",
        },
        {
            "code": "submission_approval_report",
            "name_np": "प्रस्ताव स्वीकृति रिपोर्ट",
            "text": "Submission Approval Report",
        },
        {
            "code": "comparitive_chart_report",
            "name_np": "तुलनात्मक तालिका रिपोर्ट",
            "text": "Comparitive Chart Report",
        },
    ]

    db_alias = schema_editor.connection.alias
    for report_type in report_types:
        if (
            not ReportType.objects.using(db_alias)
            .filter(
                code=report_type["code"],
            )
            .exists()
        ):
            ReportType.objects.using(db_alias).create(
                code=report_type["code"],
                name=report_type["name_np"],
                name_eng=report_type["text"],
            )


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0031_customreporttemplate_code"),
        ("plan_execution", "0079_populate_startpms_process"),
    ]

    operations = [
        migrations.RunPython(populate_report_types),
        migrations.RunPython(populate_deposit_field_mappings),
        migrations.RunPython(populate_quot_spec_mappings),
        migrations.RunPython(populate_quot_sa_mappings),
    ]
