# Generated by Django 4.2.1 on 2023-12-15 04:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0051_consumercommitteemember_member_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="consumercommitteemember",
            name="country",
        ),
        migrations.RemoveField(
            model_name="consumercommitteemember",
            name="language",
        ),
        migrations.RemoveField(
            model_name="consumercommitteemember",
            name="nationality",
        ),
        migrations.RemoveField(
            model_name="consumercommitteemember",
            name="religion",
        ),
    ]
