# Generated by Django 4.2.1 on 2023-06-17 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("budget_process", "0003_delete_estimatedfinancearrangement"),
    ]

    operations = [
        migrations.RenameField(
            model_name="incomebudgetrangedetermine",
            old_name="income_title",
            new_name="parent",
        ),
    ]
