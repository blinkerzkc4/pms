from django.db import migrations, models

from project_report.models import ReportType as ReportTypeModel


def populate_report_types(apps, schema_editor):
    ReportType: ReportTypeModel = apps.get_model("project_report", "ReportType")
    report_types = [
        {
            "code": "nikasha_report_btn_1",
            "name_np": "निकासा रिपोर्ट १",
            "text": "Nikasha Report 1",
        },
        {
            "code": "nikasha_report_btn_2",
            "name_np": "निकासा रिपोर्ट २",
            "text": "Nikasha Report 2",
        },
        {
            "code": "nikasha_report_btn_3",
            "name_np": "निकासा रिपोर्ट ३",
            "text": "Nikasha Report 3",
        },
        {
            "code": "nikasha_report_btn_4",
            "name_np": "निकासा रिपोर्ट ४",
            "text": "Nikasha Report 4",
        },
        {
            "code": "nikasha_report_btn_5",
            "name_np": "निकासा रिपोर्ट ५",
            "text": "Nikasha Report 5",
        },
        {
            "code": "nikasha_request_record",
            "name_np": "निकासा अनुरोध रेकर्ड",
            "text": "Nikasha Request Record",
        },
        {
            "code": "main_letter_head",
            "name_np": "मुख्य पत्र शीर्षक",
            "text": "Main Letter Head",
        },
        {
            "code": "department_letter_head",
            "name_np": "विभाग पत्र शीर्षक",
            "text": "Department Letter Head",
        },
        {
            "code": "ward_letter_head",
            "name_np": "वडा पत्र शीर्षक",
            "text": "Ward Letter Head",
        },
    ]

    db_alias = schema_editor.connection.alias
    for report_type in report_types:
        ReportType.objects.using(db_alias).create(
            code=report_type["code"],
            name=report_type["name_np"],
            name_eng=report_type["text"],
        )


class Migration(migrations.Migration):
    dependencies = [
        ("project_report", "0021_templatefieldmapping_db_column_name"),
    ]

    operations = [
        migrations.RunPython(populate_report_types),
    ]
