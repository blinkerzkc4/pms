from django.db import migrations


def populate_membership_type(apps, schema_editor):
    MemberType = apps.get_model("project_planning", "MemberType")
    membertypes_data = [
        {
            "code": "chairman",
            "name": "अध्यक्ष",
            "name_eng": "Chairman",
        },
        {
            "code": "vicechairman",
            "name": "उपाध्यक्ष",
            "name_eng": "Vice President",
        },
        {
            "code": "secretary",
            "name": "सचिव",
            "name_eng": "Secretary",
        },
        {
            "code": "treasurer",
            "name": "कोषाध्यक्ष",
            "name_eng": "Treasurer",
        },
        {
            "code": "member",
            "name": "सदस्य",
            "name_eng": "Member",
        },
    ]
    db_alias = schema_editor.connection.alias
    MemberType.objects.using(db_alias).all().delete()
    for membertype in membertypes_data:
        MemberType.objects.using(db_alias).create(**membertype)


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0054_alter_accounttitlemanagement_status_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_membership_type),
    ]
