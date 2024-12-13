# Generated by Django 4.2.1 on 2024-01-05 08:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_planning", "0055_populate_membership_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="consumercommitteedocument",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=55,
                null=True,
                verbose_name="Code",
            ),
        ),
    ]
