# Generated by Django 4.2.1 on 2024-06-01 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget_process", "0028_alter_approveprocess_approved_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="estimatefinancialarrangements",
            name="verfication_status",
            field=models.CharField(
                choices=[
                    ("na", "Not Applicable"),
                    ("not_submitted", "Not Submitted"),
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("req_revision", "Requires Revision"),
                    ("rejected", "Rejected"),
                ],
                default="na",
                help_text="सत्यापन स्थिति",
                max_length=55,
                verbose_name="Verification Status",
            ),
        ),
        migrations.AddField(
            model_name="expensebudgetrangedetermine",
            name="verfication_status",
            field=models.CharField(
                choices=[
                    ("na", "Not Applicable"),
                    ("not_submitted", "Not Submitted"),
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("req_revision", "Requires Revision"),
                    ("rejected", "Rejected"),
                ],
                default="na",
                help_text="सत्यापन स्थिति",
                max_length=55,
                verbose_name="Verification Status",
            ),
        ),
        migrations.AddField(
            model_name="incomebudgetrangedetermine",
            name="verfication_status",
            field=models.CharField(
                choices=[
                    ("na", "Not Applicable"),
                    ("not_submitted", "Not Submitted"),
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("req_revision", "Requires Revision"),
                    ("rejected", "Rejected"),
                ],
                default="na",
                help_text="सत्यापन स्थिति",
                max_length=55,
                verbose_name="Verification Status",
            ),
        ),
    ]