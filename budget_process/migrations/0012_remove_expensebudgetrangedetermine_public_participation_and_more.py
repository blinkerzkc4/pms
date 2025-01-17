# Generated by Django 4.2.3 on 2023-08-11 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budget_process", "0011_budgetammendment_rakam_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="expensebudgetrangedetermine",
            name="public_participation",
        ),
        migrations.AddField(
            model_name="expensebudgetrangedetermine",
            name="is_budget_estimates",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="source",
            name="public_participation",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
