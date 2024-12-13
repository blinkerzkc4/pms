from django.db import migrations, models


def populate_work_class_model(apps, schema_editor):
    WorkClass = apps.get_model("formulate_plan", "WorkClass")
    work_class_data = [
        {
            "code": "eco_dev",
            "name": "आर्थिक विकास",
            "name_eng": "Economic Development",
        },
        {
            "code": "infra_dev",
            "name": "पूर्वाधार विकास",
            "name_eng": "Infrastructure Development",
        },
        {
            "code": "social_dev",
            "name": "सामाजिक विकास",
            "name_eng": "Social Development",
        },
        {
            "code": "env_dis",
            "name": "वातावरण तथा विपद व्यवस्थापन",
            "name_eng": "Environment and Disaster Management",
        },
        {
            "code": "inst_dev",
            "name": "संस्थागत विकास",
            "name_eng": "Institutional Development",
        },
        {
            "code": "ser_gov",
            "name": "सेवा पवाह र सुशासन",
            "name_eng": "Service Delivery and Governance",
        },
    ]
    db_alias = schema_editor.connection.alias
    for work_class in work_class_data:
        WorkClass.objects.using(db_alias).create(**work_class)


class Migration(migrations.Migration):
    dependencies = [
        ("formulate_plan", "0015_alter_budgetassurance_amount_and_more"),
    ]

    operations = [
        migrations.RunPython(
            populate_work_class_model, reverse_code=migrations.RunPython.noop
        ),
    ]
