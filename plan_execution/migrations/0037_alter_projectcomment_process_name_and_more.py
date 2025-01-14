# Generated by Django 4.2.1 on 2023-11-20 05:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plan_execution", "0036_projectcommentremarkfile_projectcomment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectcomment",
            name="process_name",
            field=models.CharField(
                blank=True,
                choices=[
                    ("म्याद थप", "म्याद थप"),
                    ("निकासा", "निकासा"),
                    ("इस्टिमेट पेश/स्वीकृत सम्बन्धि", "इस्टिमेट पेश/स्वीकृत सम्बन्धि"),
                    ("मोबिलैजेशन", "मोबिलैजेशन"),
                    ("योजना संशोधन", "योजना संशोधन"),
                    ("कार्य सम्पन्न विवरण", "कार्य सम्पन्न विवरण"),
                    ("नापी किताब सम्बन्धि", "नापी किताब सम्बन्धि"),
                    ("टेन्डर सम्बन्धि", "टेन्डर सम्बन्धि"),
                    ("बोलपत्र संकलन", "बोलपत्र संकलन"),
                    ("दरभाउ पत्र/बोलपत्र स्वीकृत", "दरभाउ पत्र/बोलपत्र स्वीकृत"),
                    ("सम्झौता सम्बन्धि", "सम्झौता सम्बन्धि"),
                    ("निकासा विल भुक्तानी सम्बन्धि", "निकासा विल भुक्तानी सम्बन्धि"),
                    ("उपभोक्ता छनौट/गठन", "उपभोक्ता छनौट/गठन"),
                    ("सम्भाव्यता अध्ययन/स्वीकृत", "सम्भाव्यता अध्ययन/स्वीकृत"),
                    ("सम्झौता/खाता खोलिदिन सम्बन्धि", "सम्झौता/खाता खोलिदिन सम्बन्धि"),
                    ("अनुगमन", "अनुगमन"),
                    ("टिप्पणी र आदेश", "टिप्पणी र आदेश"),
                    ("अमानत कार्यादेश", "अमानत कार्यादेश"),
                    ("कार्य सम्पन्न तथा फरफारक", "कार्य सम्पन्न तथा फरफारक"),
                    ("मनोनित कर्मचारी", "मनोनित कर्मचारी"),
                    ("कार्यादेश", "कार्यादेश"),
                ],
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="projectcomment",
            name="status",
            field=models.CharField(
                choices=[("P", "Pending"), ("A", "Approved"), ("R", "Rejected")],
                default="P",
                max_length=1,
            ),
        ),
    ]
