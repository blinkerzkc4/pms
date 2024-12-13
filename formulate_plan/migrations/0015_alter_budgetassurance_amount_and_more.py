# Generated by Django 4.2.1 on 2023-11-23 18:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0055_alter_district_code_alter_district_created_by_and_more"),
        ("project_planning", "0041_alter_accounttitlemanagement_code_and_more"),
        ("budget_process", "0021_alter_approveprocess_approved_by_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("employee", "0016_alter_country_code_alter_country_created_by_and_more"),
        (
            "base_model",
            "0012_alter_address_created_by_alter_address_created_date_and_more",
        ),
        ("formulate_plan", "0014_alter_workproject_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budgetassurance",
            name="amount",
            field=models.CharField(
                blank=True,
                help_text="रकम",
                max_length=50,
                null=True,
                verbose_name="Amount",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="approved_by",
            field=models.ForeignKey(
                blank=True,
                help_text="स्वीकृत गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="employee.employee",
                verbose_name="Approved By",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="approved_date",
            field=models.CharField(
                blank=True,
                help_text="स्वीकृत मिति",
                max_length=50,
                null=True,
                verbose_name="Approved Date",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="approved_date_eng",
            field=models.CharField(
                blank=True,
                help_text="स्वीकृत मिति (अंग्रेजी)",
                max_length=50,
                null=True,
                verbose_name="Approved Date (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
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
            model_name="budgetassurance",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="current_fy_budget",
            field=models.CharField(
                blank=True,
                help_text="चालु आर्थिक बर्ष बजेट",
                max_length=50,
                null=True,
                verbose_name="Current Fiscal Year Budget",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="current_fy_outcome",
            field=models.CharField(
                blank=True,
                help_text="चालु आर्थिक बर्ष परिणाम",
                max_length=50,
                null=True,
                verbose_name="Current Fiscal Year Outcome",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="expense_title_name",
            field=models.ForeignKey(
                blank=True,
                help_text="खर्च शीर्षक नाम",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project_planning.expansetype",
                verbose_name="Expense Title Name",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="expense_title_no",
            field=models.CharField(
                blank=True,
                help_text="खर्च शीर्षक नं.",
                max_length=50,
                null=True,
                verbose_name="Expense Title No",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="first_quarter_budget",
            field=models.CharField(
                blank=True,
                help_text="पहिलो तिमाही बजेट",
                max_length=50,
                null=True,
                verbose_name="First Quarter Budget",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="first_quarter_outcome",
            field=models.CharField(
                blank=True,
                help_text="पहिलो तिमाही परिणाम",
                max_length=50,
                null=True,
                verbose_name="First Quarter Outcome",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="internal_source",
            field=models.CharField(
                blank=True,
                help_text="आन्तरिक स्रोत",
                max_length=50,
                null=True,
                verbose_name="Internal Source",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="loan_source",
            field=models.CharField(
                blank=True,
                help_text="कर्जा स्रोत",
                max_length=50,
                null=True,
                verbose_name="Loan Source",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="local_level_source",
            field=models.CharField(
                blank=True,
                help_text="स्थानीय तहको स्रोत",
                max_length=50,
                null=True,
                verbose_name="Local Level Source",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="nepal_gov_source",
            field=models.CharField(
                blank=True,
                help_text="नेपाल सरकारको स्रोत",
                max_length=50,
                null=True,
                verbose_name="Nepal Government Source",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="past_fiscal_year_expense",
            field=models.CharField(
                blank=True,
                help_text="गत आर्थिक बर्ष खर्च",
                max_length=50,
                null=True,
                verbose_name="Past Fiscal Year Expense",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="past_fiscal_year_outcome",
            field=models.CharField(
                blank=True,
                help_text="गत आर्थिक बर्ष परिणाम",
                max_length=50,
                null=True,
                verbose_name="Past Fiscal Year Outcome",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="program_activity_outcome",
            field=models.CharField(
                blank=True,
                help_text="कार्यक्रम गतिविधि परिणाम",
                max_length=50,
                null=True,
                verbose_name="Program Activity Outcome",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="province_source",
            field=models.CharField(
                blank=True,
                help_text="प्रदेश सरकारको स्रोत",
                max_length=50,
                null=True,
                verbose_name="Province Source",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="public_participation_source",
            field=models.CharField(
                blank=True,
                help_text="सार्वजनिक सहभागिता स्रोत",
                max_length=50,
                null=True,
                verbose_name="Public Participation Source",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="second_quarter_budget",
            field=models.CharField(
                blank=True,
                help_text="दोस्रो तिमाही बजेट",
                max_length=50,
                null=True,
                verbose_name="Second Quarter Budget",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="second_quarter_outcome",
            field=models.CharField(
                blank=True,
                help_text="दोस्रो तिमाही परिणाम",
                max_length=50,
                null=True,
                verbose_name="Second Quarter Outcome",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="third_quarter_budget",
            field=models.CharField(
                blank=True,
                help_text="तेस्रो तिमाही बजेट",
                max_length=50,
                null=True,
                verbose_name="Third Quarter Budget",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="third_quarter_outcome",
            field=models.CharField(
                blank=True,
                help_text="तेस्रो तिमाही परिणाम",
                max_length=50,
                null=True,
                verbose_name="Third Quarter Outcome",
            ),
        ),
        migrations.AlterField(
            model_name="budgetassurance",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="projectdocument",
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
            model_name="projectdocument",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="projectdocument",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="projectworktype",
            name="class_of_work",
            field=models.ForeignKey(
                blank=True,
                help_text="कामको वर्ग",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="formulate_plan.workclass",
                verbose_name="Class of Work",
            ),
        ),
        migrations.AlterField(
            model_name="projectworktype",
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
            model_name="projectworktype",
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
            model_name="projectworktype",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="projectworktype",
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
            model_name="projectworktype",
            name="kramagat",
            field=models.IntegerField(
                blank=True, help_text="क्रमागत", null=True, verbose_name="Kramagat"
            ),
        ),
        migrations.AlterField(
            model_name="projectworktype",
            name="max_budget",
            field=models.IntegerField(
                blank=True,
                help_text="अधिकतम बजेट",
                null=True,
                verbose_name="Max Budget",
            ),
        ),
        migrations.AlterField(
            model_name="projectworktype",
            name="min_budget",
            field=models.IntegerField(
                blank=True,
                help_text="न्यूनतम बजेट",
                null=True,
                verbose_name="Min Budget",
            ),
        ),
        migrations.AlterField(
            model_name="projectworktype",
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
            model_name="projectworktype",
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
            model_name="projectworktype",
            name="overall_priority",
            field=models.CharField(
                blank=True,
                help_text="समग्र प्राथमिकता",
                max_length=100,
                null=True,
                verbose_name="Overall Priority",
            ),
        ),
        migrations.AlterField(
            model_name="projectworktype",
            name="priority_class",
            field=models.CharField(
                blank=True,
                help_text="प्राथमिकता वर्ग",
                max_length=100,
                null=True,
                verbose_name="Priority Class",
            ),
        ),
        migrations.AlterField(
            model_name="projectworktype",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="projectworktype",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="workclass",
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
            model_name="workclass",
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
            model_name="workclass",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="workclass",
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
            model_name="workclass",
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
            model_name="workclass",
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
            model_name="workclass",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="workclass",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="achievement",
            field=models.CharField(
                blank=True,
                help_text="अधिगम",
                max_length=40,
                null=True,
                verbose_name="Achievement",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="address",
            field=models.ForeignKey(
                blank=True,
                help_text="ठेगाना",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="base_model.address",
                verbose_name="Address",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="approve",
            field=models.ForeignKey(
                blank=True,
                help_text="अनुमोदन प्रक्रिया",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="budget_process.approveprocess",
                verbose_name="Approve Process",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="approved_date",
            field=models.CharField(
                blank=True,
                help_text="स्वीकृत मिति",
                max_length=50,
                null=True,
                verbose_name="Approved Date",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="approved_date_eng",
            field=models.CharField(
                blank=True,
                help_text="स्वीकृत मिति (अंग्रेजी)",
                max_length=50,
                null=True,
                verbose_name="Approved Date (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="benefited_households",
            field=models.CharField(
                blank=True,
                help_text="लाभान्वित घरधुरीहरु",
                max_length=40,
                null=True,
                verbose_name="Benefited Households",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="benefited_population",
            field=models.CharField(
                blank=True,
                help_text="लाभान्वित जनसंख्या",
                max_length=40,
                null=True,
                verbose_name="Benefited Population",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="budget_assurance",
            field=models.ForeignKey(
                blank=True,
                help_text="बजेट आश्वासन",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="formulate_plan.budgetassurance",
                verbose_name="Budget Assurance",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
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
            model_name="workproject",
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
            model_name="workproject",
            name="created_date",
            field=models.DateTimeField(
                auto_now_add=True, help_text="निर्माण मिति", verbose_name="Created Date"
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
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
            model_name="workproject",
            name="estimated_amount",
            field=models.CharField(
                blank=True,
                help_text="अनुमानित रकम",
                max_length=40,
                null=True,
                verbose_name="Estimated Amount",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="estimated_end_date",
            field=models.CharField(
                blank=True,
                help_text="अनुमानित समापन मिति",
                max_length=40,
                null=True,
                verbose_name="Estimated End Date",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="estimated_end_date_eng",
            field=models.CharField(
                blank=True,
                help_text="अनुमानित समापन मिति (अंग्रेजी)",
                max_length=40,
                null=True,
                verbose_name="Estimated End Date (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="estimated_start_date",
            field=models.CharField(
                blank=True,
                help_text="अनुमानित सुरु मिति",
                max_length=40,
                null=True,
                verbose_name="Estimated Start Date",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="estimated_start_date_eng",
            field=models.CharField(
                blank=True,
                help_text="अनुमानित सुरु मिति (अंग्रेजी)",
                max_length=40,
                null=True,
                verbose_name="Estimated Start Date (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="financial_year",
            field=models.ForeignKey(
                blank=True,
                help_text="आर्थिक बर्ष ",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="financial_year",
                to="project.financialyear",
                verbose_name="Financial Year",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="internal_source",
            field=models.CharField(
                blank=True,
                help_text="आन्तरिक स्रोत",
                max_length=40,
                null=True,
                verbose_name="Internal Source",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="is_approved",
            field=models.BooleanField(
                blank=True,
                default=False,
                help_text="स्वीकृत गरिएको छ",
                null=True,
                verbose_name="Is Approved",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="is_prioritized",
            field=models.BooleanField(
                blank=True,
                default=False,
                help_text="प्राथमिकतामा राखिएको छ",
                null=True,
                verbose_name="Is Prioritized",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="kramagat",
            field=models.CharField(
                blank=True,
                help_text="क्रमागत",
                max_length=150,
                null=True,
                verbose_name="Kramagat",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="loan",
            field=models.CharField(
                blank=True,
                help_text="कर्जा",
                max_length=40,
                null=True,
                verbose_name="Loan",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="local_level_gov",
            field=models.CharField(
                blank=True,
                help_text="स्थानीय तह",
                max_length=40,
                null=True,
                verbose_name="Local Level Government",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="योजनाको नाम",
                max_length=500,
                null=True,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="name_eng",
            field=models.CharField(
                blank=True,
                help_text="योजनाको नाम (अंग्रेजी)",
                max_length=255,
                null=True,
                verbose_name="Name (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="nepal_gov",
            field=models.CharField(
                blank=True,
                help_text="नेपाल सरकार",
                max_length=40,
                null=True,
                verbose_name="Nepal Government",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="priority_approved_by",
            field=models.ForeignKey(
                blank=True,
                help_text="प्राथमिकता स्वीकृत गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="priority_approved_by",
                to="employee.employee",
                verbose_name="Priority Approved By",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="priority_approved_date",
            field=models.CharField(
                blank=True,
                help_text="प्राथमिकता स्वीकृत मिति",
                max_length=50,
                null=True,
                verbose_name="Priority Approved Date",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="priority_approved_date_eng",
            field=models.CharField(
                blank=True,
                help_text="प्राथमिकता स्वीकृत मिति (अंग्रेजी)",
                max_length=50,
                null=True,
                verbose_name="Priority Approved Date (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="project_approved_by",
            field=models.ForeignKey(
                blank=True,
                help_text="योजना स्वीकृत गर्ने",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="project_approved_by",
                to="employee.employee",
                verbose_name="Project Approved By",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="project_approved_date",
            field=models.CharField(
                blank=True,
                help_text="योजना स्वीकृत मिति",
                max_length=50,
                null=True,
                verbose_name="Project Approved Date",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="project_approved_date_eng",
            field=models.CharField(
                blank=True,
                help_text="योजना स्वीकृत मिति (अंग्रेजी)",
                max_length=50,
                null=True,
                verbose_name="Project Approved Date (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="project_level",
            field=models.ForeignKey(
                blank=True,
                help_text="योजनाको स्तर",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project_planning.projectlevel",
                verbose_name="Project Level",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="project_prioritization",
            field=models.ForeignKey(
                blank=True,
                help_text="प्राथमिकताको प्रकार",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project_planning.prioritytype",
                verbose_name="Project Prioritization",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="proposed_date",
            field=models.CharField(
                blank=True,
                help_text="प्रस्तावित मिति",
                max_length=40,
                null=True,
                verbose_name="Proposed Date",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="proposed_date_eng",
            field=models.CharField(
                blank=True,
                help_text="प्रस्तावित मिति (अंग्रेजी)",
                max_length=40,
                null=True,
                verbose_name="Proposed Date (Eng)",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="proposed_financial_year",
            field=models.ForeignKey(
                blank=True,
                help_text="प्रस्तावित आर्थिक बर्ष ",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="proposed_fy",
                to="project.financialyear",
                verbose_name="Proposed Financial Year",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="proposed_project_outcome",
            field=models.CharField(
                blank=True,
                help_text="प्रस्थाबित योजना/कार्यक्रमको परिणाम",
                max_length=200,
                null=True,
                verbose_name="Proposed Project Outcome",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="proposed_type",
            field=models.ForeignKey(
                blank=True,
                help_text="योजनाको प्रस्ताबित प्रकार",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project_planning.projectproposedtype",
                verbose_name="Proposed Type",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="proposed_unit_type",
            field=models.ForeignKey(
                blank=True,
                help_text="प्रस्थाबित योजना/कार्यक्रम को प्रकार",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="proposed_unit_type",
                to="project.unit",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="province_gov",
            field=models.CharField(
                blank=True,
                help_text="प्रदेश सरकार",
                max_length=40,
                null=True,
                verbose_name="Province Government",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="public_participation",
            field=models.CharField(
                blank=True,
                help_text="सार्वजनिक सहभागिता",
                max_length=40,
                null=True,
                verbose_name="Public Participation",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="remarks",
            field=models.CharField(
                blank=True,
                help_text="कैफियत",
                max_length=150,
                null=True,
                verbose_name="Remarks",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="status",
            field=models.BooleanField(
                default=True, help_text="स्थिति", verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="updated_date",
            field=models.DateTimeField(
                auto_now=True, help_text="अद्यावधिक मिति", verbose_name="Updated Date"
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="user_committee",
            field=models.ForeignKey(
                blank=True,
                help_text=" उपभोक्ता समिति",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project_planning.consumercommittee",
                verbose_name="User Committee",
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="ward",
            field=models.IntegerField(
                blank=True, help_text="वडा नं. ", null=True, verbose_name="Ward No."
            ),
        ),
        migrations.AlterField(
            model_name="workproject",
            name="work_class",
            field=models.ForeignKey(
                blank=True,
                help_text="कामको वर्ग",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="formulate_plan.workclass",
                verbose_name="Work Class",
            ),
        ),
    ]
