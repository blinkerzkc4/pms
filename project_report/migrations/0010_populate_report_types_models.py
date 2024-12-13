from django.db import migrations, models

from project_report.models import ReportType as ReportTypeModel


def populate_report_types(apps, schema_editor):
    ReportType: ReportTypeModel = apps.get_model("project_report", "ReportType")
    report_types = [
        {
            "id": 12,
            "value": 12,
            "code": "acc_close_patra_btn",
            "name_np": "खाता बन्द गर्ने पत्र",
            "text": "acc_close_patra_btn - खाता बन्द गर्ने पत्र",
        },
        {
            "id": 5,
            "value": 5,
            "code": "acc_open_report_btn",
            "name_np": "बैंक खाता खोलिदिने रिपोर्ट",
            "text": "acc_open_report_btn - बैंक खाता खोलिदिने रिपोर्ट",
        },
        {
            "id": 4,
            "value": 4,
            "code": "aggreement_call_work_order_btn",
            "name_np": "उपभोक्ता बोधार्थ",
            "text": "aggreement_call_work_order_btn - उपभोक्ता बोधार्थ",
        },
        {
            "id": 10,
            "value": 10,
            "code": "agreement_presence_btn",
            "name_np": "सम्झौता उपस्थित प्रतिबेदन",
            "text": "agreement_presence_btn - सम्झौता उपस्थित प्रतिबेदन",
        },
        {
            "id": 9,
            "value": 9,
            "code": "agreement_report_btn",
            "name_np": "सम्झौता प्रतिबेदन",
            "text": "agreement_report_btn - सम्झौता प्रतिबेदन",
        },
        {
            "id": 3,
            "value": 3,
            "code": "call_agreement_presence_report_btn",
            "name_np": "उपभोक्ता बोधार्थ १",
            "text": "call_agreement_presence_report_btn - उपभोक्ता बोधार्थ १",
        },
        {
            "id": 1,
            "value": 1,
            "code": "contract_agreement_btn",
            "name_np": "उपभोक्ता समिति सम्झौता पत्र -1",
            "text": "contract_agreement_btn - उपभोक्ता समिति सम्झौता पत्र -1",
        },
        {
            "id": 2,
            "value": 2,
            "code": "contract_agreement_btn_two",
            "name_np": "उपभोक्ता समिति सम्झौता पत्र -2",
            "text": "contract_agreement_btn_two - उपभोक्ता समिति सम्झौता पत्र -2",
        },
        {
            "id": 23,
            "value": 23,
            "code": "contract_letter_bidbon",
            "name_np": "दरभाउ पत्र/बोलपत्र अनुसारको सम्झौता उपस्थित पत्र",
            "text": "contract_letter_bidbon - दरभाउ पत्र/बोलपत्र अनुसारको सम्झौता उपस्थित पत्र",
        },
        {
            "id": 22,
            "value": 22,
            "code": "contract_letter_normal",
            "name_np": "सम्झौताको लागि उपस्थित पत्र",
            "text": "contract_letter_normal - सम्झौताको लागि उपस्थित पत्र",
        },
        {
            "id": 24,
            "value": 24,
            "code": "contract_work_order_lette",
            "name_np": "कार्यादेश पत्र",
            "text": "contract_work_order_lette - कार्यादेश पत्र",
        },
        {
            "id": 11,
            "value": 11,
            "code": "different_pdf_btn",
            "name_np": "फरफारक प्रतिबेदन",
            "text": "different_pdf_btn - फरफारक प्रतिबेदन",
        },
        {
            "id": 15,
            "value": 15,
            "code": "estimate_submit_report",
            "name_np": "इस्टिमेट प्रतिबेदन",
            "text": "estimate_submit_report - इस्टिमेट प्रतिबेदन",
        },
        {
            "id": 8,
            "value": 8,
            "code": "feasibility_approve_report",
            "name_np": "सम्भाभ्यता अध्यन प्रतिबेदन",
            "text": "feasibility_approve_report - सम्भाभ्यता अध्यन प्रतिबेदन",
        },
        {
            "id": 21,
            "value": 21,
            "code": "letter_approval_bid_approved_report",
            "name_np": "दरभाउ पत्र/बोलपत्र स्वीकृत प्रतिबेदन",
            "text": "letter_approval_bid_approved_report - दरभाउ पत्र/बोलपत्र स्वीकृत प्रतिबेदन",
        },
        {
            "id": 14,
            "value": 14,
            "code": "mobilization_report",
            "name_np": "मोबिलाईजेसन प्रतिबेदन",
            "text": "mobilization_report - मोबिलाईजेसन प्रतिबेदन",
        },
        {
            "id": 28,
            "value": 28,
            "code": "mobilization_report_contract",
            "name_np": "मोबिलाईजेसन प्रतिबेदन",
            "text": "mobilization_report_contract - मोबिलाईजेसन प्रतिबेदन",
        },
        {
            "id": 29,
            "value": 29,
            "code": "monitoring_report_one",
            "name_np": "अनुगमन समिति प्रतिबेदन 1",
            "text": "monitoring_report_one - अनुगमन समिति प्रतिबेदन 1",
        },
        {
            "id": 30,
            "value": 30,
            "code": "monitoring_report_two",
            "name_np": "अनुगमन समिति प्रतिबेदन 2",
            "text": "monitoring_report_two - अनुगमन समिति प्रतिबेदन 2",
        },
        {
            "id": 19,
            "value": 19,
            "code": "news_post_the_information",
            "name_np": "सूचना टाँस गरि मुचुल्का पठठाईदिने प्रतिबेदन",
            "text": "news_post_the_information - सूचना टाँस गरि मुचुल्का पठठाईदिने प्रतिबेदन",
        },
        {
            "id": 18,
            "value": 18,
            "code": "news_publish_report",
            "name_np": "सूचना प्रकाशित गरिदिने प्रतिबेदन",
            "text": "news_publish_report - सूचना प्रकाशित गरिदिने प्रतिबेदन",
        },
        {
            "id": 13,
            "value": 13,
            "code": "nikasha_report_btn",
            "name_np": "निकाशा प्रतिबेदन",
            "text": "nikasha_report_btn - निकाशा प्रतिबेदन",
        },
        {
            "id": 6,
            "value": 6,
            "code": "notice_published",
            "name_np": "आवेदन माग सार्बजनिक सूचना",
            "text": "notice_published - आवेदन माग सार्बजनिक सूचना",
        },
        {
            "id": 26,
            "value": 26,
            "code": "notice_toward_tender_applier_report",
            "name_np": "दरभाउपत्र/बोलपत्र स्वीकृतिको आशयपत्र सम्बन्धी सूचना",
            "text": "notice_toward_tender_applier_report - दरभाउपत्र/बोलपत्र स्वीकृतिको आशयपत्र सम्बन्धी सूचना",
        },
        {
            "id": 7,
            "value": 7,
            "code": "opinion_report",
            "name_np": "योजना माग सम्बन्ध",
            "text": "opinion_report - योजना माग सम्बन्ध",
        },
        {
            "id": 31,
            "value": 31,
            "code": "overdue_reporting",
            "name_np": "म्याद थप प्रतिबेदन",
            "text": "overdue_reporting - म्याद थप प्रतिबेदन",
        },
        {
            "id": 25,
            "value": 25,
            "code": "refund_report",
            "name_np": "refund report",
            "text": "refund_report - refund report",
        },
        {
            "id": 20,
            "value": 20,
            "code": "report_to_be_sent_by_the_representative",
            "name_np": "प्रतिनिधि पठाईदिने प्रतिबेदन",
            "text": "report_to_be_sent_by_the_representative - प्रतिनिधि पठाईदिने प्रतिबेदन",
        },
        {
            "id": 32,
            "value": 32,
            "code": "somsodhan_report",
            "name_np": "संशोधन विवरण पि्रन्ट प्रतिबेदन",
            "text": "somsodhan_report - संशोधन विवरण पि्रन्ट प्रतिबेदन",
        },
        {
            "id": 17,
            "value": 17,
            "code": "tender_notice_report",
            "name_np": "टेन्डर नोटिश प्रतिबेदन",
            "text": "tender_notice_report - टेन्डर नोटिश प्रतिबेदन",
        },
        {
            "id": 27,
            "value": 27,
            "code": "tippani_report_btn",
            "name_np": "टिप्पणी आदेश प्रतिवेदन",
            "text": "tippani_report_btn - टिप्पणी आदेश प्रतिवेदन",
        },
        {
            "id": 34,
            "value": 34,
            "code": "work_order_biniyojit_tipani",
            "name_np": "विनियोजित रकम टिप्पणी",
            "text": "work_order_biniyojit_tipani - विनियोजित रकम टिप्पणी",
        },
        {
            "id": 36,
            "value": 36,
            "code": "work_order_compleate_payment_tipani",
            "name_np": "भुक्तानी तथा फरफारक सम्बन्धमा",
            "text": "work_order_compleate_payment_tipani - भुक्तानी तथा फरफारक सम्बन्धमा",
        },
        {
            "id": 35,
            "value": 35,
            "code": "work_order_mandate_tipani",
            "name_np": "कार्यादेश",
            "text": "work_order_mandate_tipani - कार्यादेश",
        },
        {
            "id": 33,
            "value": 33,
            "code": "work_order_toka_tipani",
            "name_np": "तोक आदेश टिप्पणी",
            "text": "work_order_toka_tipani - तोक आदेश टिप्पणी",
        },
        {
            "id": 16,
            "value": 16,
            "code": "work_staff_report_button",
            "name_np": "कार्यदेश प्रतिबेदन",
            "text": "work_staff_report_button - कार्यदेश प्रतिबेदन",
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
        ("project_report", "0009_alter_customreporttemplate_status_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_report_types),
    ]
