# Generated by Django 4.2.1 on 2023-11-03 03:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget_process", "0018_remove_budgetexpensemanagement_parent_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budgetexpensemanagement",
            name="activity_name",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
