# Generated by Django 4.2.1 on 2023-11-23 18:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("employee", "0016_alter_country_code_alter_country_created_by_and_more"),
        ("budget_process", "0020_budgetexpensemanagement_municipality"),
    ]

    operations = [
        migrations.AlterField(
            model_name="approveprocess",
            name="approved_by",
            field=models.ForeignKey(
                blank=True,
                help_text="द्वारा स्वीकृत",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="a_employee",
                to="employee.employee",
                verbose_name="Approved By",
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="approved_date",
            field=models.CharField(
                blank=True,
                help_text="स्वीकृत मिति",
                max_length=100,
                null=True,
                verbose_name="Approved Date",
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="approved_date_eng",
            field=models.CharField(
                blank=True,
                help_text="स्वीकृत मिति (अंग्रेजी)",
                max_length=100,
                null=True,
                verbose_name="Approved Date (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="is_approved",
            field=models.BooleanField(
                default=False, help_text="स्वीकृत गरियो", verbose_name="Approved"
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="is_prepared",
            field=models.BooleanField(
                default=False, help_text="तयार भयो", verbose_name="Prepared"
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="is_verified",
            field=models.BooleanField(
                default=False, help_text="प्रमाणित गरियो", verbose_name="Verified"
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="prepared_by",
            field=models.ForeignKey(
                blank=True,
                help_text="द्वारा तयार",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="p_employee",
                to="employee.employee",
                verbose_name="Prepared By",
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="prepared_date",
            field=models.CharField(
                blank=True,
                help_text="तयार मिति",
                max_length=100,
                null=True,
                verbose_name="Prepared Date",
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="prepared_date_eng",
            field=models.CharField(
                blank=True,
                help_text="तयार मिति (अंग्रेजी)",
                max_length=100,
                null=True,
                verbose_name="Prepared Date (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="verified_by",
            field=models.ForeignKey(
                blank=True,
                help_text="द्वारा प्रमाणित",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="v_employee",
                to="employee.employee",
                verbose_name="Verified By",
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="verified_date",
            field=models.CharField(
                blank=True,
                help_text="प्रमाणित मिति",
                max_length=100,
                null=True,
                verbose_name="Verified Date",
            ),
        ),
        migrations.AlterField(
            model_name="approveprocess",
            name="verified_date_eng",
            field=models.CharField(
                blank=True,
                help_text="प्रमाणित मिति (अंग्रेजी)",
                max_length=100,
                null=True,
                verbose_name="Verified Date (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="budgetammendment",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="budgetammendment",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="budgetammendment",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="budgetexpensemanagement",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="budgetexpensemanagement",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="budgetexpensemanagement",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="budgetmanagement",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="budgetmanagement",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="budgetmanagement",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="estimatefinancialarrangements",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=55,
                null=True,
                verbose_name="Code",
            ),
        ),
        migrations.AlterField(
            model_name="estimatefinancialarrangements",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="estimatefinancialarrangements",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="estimatefinancialarrangements",
            name="detail",
            field=models.CharField(
                blank=True,
                help_text="विवरण",
                max_length=500,
                null=True,
                verbose_name="Detail",
            ),
        ),
        migrations.AlterField(
            model_name="estimatefinancialarrangements",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="नाम",
                max_length=100,
                null=True,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="estimatefinancialarrangements",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=100,
                null=True,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="estimatefinancialarrangements",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="expensebudgetrangedetermine",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=55,
                null=True,
                verbose_name="Code",
            ),
        ),
        migrations.AlterField(
            model_name="expensebudgetrangedetermine",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="expensebudgetrangedetermine",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="expensebudgetrangedetermine",
            name="detail",
            field=models.CharField(
                blank=True,
                help_text="विवरण",
                max_length=500,
                null=True,
                verbose_name="Detail",
            ),
        ),
        migrations.AlterField(
            model_name="expensebudgetrangedetermine",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="नाम",
                max_length=100,
                null=True,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="expensebudgetrangedetermine",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=100,
                null=True,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="expensebudgetrangedetermine",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="incomebudgetrangedetermine",
            name="code",
            field=models.CharField(
                blank=True,
                help_text="कोड",
                max_length=55,
                null=True,
                verbose_name="Code",
            ),
        ),
        migrations.AlterField(
            model_name="incomebudgetrangedetermine",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="incomebudgetrangedetermine",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="incomebudgetrangedetermine",
            name="detail",
            field=models.CharField(
                blank=True,
                help_text="विवरण",
                max_length=500,
                null=True,
                verbose_name="Detail",
            ),
        ),
        migrations.AlterField(
            model_name="incomebudgetrangedetermine",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="नाम",
                max_length=100,
                null=True,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="incomebudgetrangedetermine",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="नाम (अंग्रेजी)",
                max_length=100,
                null=True,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="incomebudgetrangedetermine",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="source",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="निर्माण गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="source",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="source",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
    ]
