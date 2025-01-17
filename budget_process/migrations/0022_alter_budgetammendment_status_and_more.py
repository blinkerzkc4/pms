# Generated by Django 4.2.1 on 2023-12-17 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget_process", "0021_alter_approveprocess_approved_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budgetammendment",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="budgetexpensemanagement",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="budgetmanagement",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="budgettransfer",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="estimatefinancialarrangements",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="expensebudgetrangedetermine",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="incomebudgetrangedetermine",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name="source",
            name="status",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
