# Generated by Django 4.2.1 on 2023-12-03 09:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0048_remove_consumercommitteemember_address_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="consumercommitteedocument",
            name="code",
        ),
        migrations.RemoveField(
            model_name="consumercommitteedocument",
            name="detail",
        ),
        migrations.RemoveField(
            model_name="consumercommitteedocument",
            name="name",
        ),
        migrations.RemoveField(
            model_name="consumercommitteedocument",
            name="name_eng",
        ),
        migrations.AddField(
            model_name="consumercommitteedocument",
            name="document",
            field=models.FileField(
                default=None, upload_to="consumer_committee_documents/"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="consumercommitteedocument",
            name="document_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="consumercommitteedocument",
            name="document_size",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
