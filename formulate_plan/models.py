from django.db import models

from base_model.models import Address, CommonFieldsBase, DocumentType
from budget_process.models import ApproveProcess
from employee.models import Employee
from project.models import BaseModel, FinancialYear, Municipality, Unit
from project_planning.models import (
    ConsumerCommittee,
    ExpanseType,
    PriorityType,
    ProjectLevel,
    ProjectProposedType,
    Road,
)

# Create your models here.


class WorkClass(CommonFieldsBase):
    """
    कामको वर्ग
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectWorkType(CommonFieldsBase):
    class_of_work = models.ForeignKey(
        WorkClass,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Class of Work",
        help_text="कामको वर्ग",
    )
    priority_class = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Priority Class",
        help_text="प्राथमिकता वर्ग",
    )
    overall_priority = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Overall Priority",
        help_text="समग्र प्राथमिकता",
    )
    max_budget = models.BigIntegerField(
        null=True, blank=True, verbose_name="Max Budget", help_text="अधिकतम बजेट"
    )
    min_budget = models.BigIntegerField(
        null=True, blank=True, verbose_name="Min Budget", help_text="न्यूनतम बजेट"
    )
    kramagat = models.IntegerField(
        null=True, blank=True, verbose_name="Kramagat", help_text="क्रमागत"
    )

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class BudgetAssurance(BaseModel):
    amount = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Amount", help_text="रकम"
    )
    internal_source = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Internal Source",
        help_text="आन्तरिक स्रोत",
    )
    nepal_gov_source = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Nepal Government Source",
        help_text="नेपाल सरकारको स्रोत",
    )
    province_source = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Province Source",
        help_text="प्रदेश सरकारको स्रोत",
    )
    local_level_source = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Local Level Source",
        help_text="स्थानीय तहको स्रोत",
    )
    loan_source = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Loan Source",
        help_text="कर्जा स्रोत",
    )
    public_participation_source = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Public Participation Source",
        help_text="सार्वजनिक सहभागिता स्रोत",
    )
    expense_title_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Expense Title No",
        help_text="खर्च शीर्षक नं.",
    )
    expense_title_name = models.ForeignKey(
        ExpanseType,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Expense Title Name",
        help_text="खर्च शीर्षक नाम",
    )
    program_activity_outcome = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Program Activity Outcome",
        help_text="कार्यक्रम गतिविधि परिणाम",
    )
    past_fiscal_year_outcome = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Past Fiscal Year Outcome",
        help_text="गत आर्थिक बर्ष परिणाम",
    )
    past_fiscal_year_expense = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Past Fiscal Year Expense",
        help_text="गत आर्थिक बर्ष खर्च",
    )
    current_fy_outcome = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Current Fiscal Year Outcome",
        help_text="चालु आर्थिक बर्ष परिणाम",
    )
    current_fy_budget = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Current Fiscal Year Budget",
        help_text="चालु आर्थिक बर्ष बजेट",
    )
    first_quarter_outcome = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="First Quarter Outcome",
        help_text="पहिलो तिमाही परिणाम",
    )
    first_quarter_budget = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="First Quarter Budget",
        help_text="पहिलो तिमाही बजेट",
    )
    second_quarter_outcome = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Second Quarter Outcome",
        help_text="दोस्रो तिमाही परिणाम",
    )
    second_quarter_budget = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Second Quarter Budget",
        help_text="दोस्रो तिमाही बजेट",
    )
    third_quarter_outcome = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Third Quarter Outcome",
        help_text="तेस्रो तिमाही परिणाम",
    )
    third_quarter_budget = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Third Quarter Budget",
        help_text="तेस्रो तिमाही बजेट",
    )
    approved_by = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Approved By",
        help_text="स्वीकृत गर्ने",
    )
    approved_date = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Approved Date",
        help_text="स्वीकृत मिति",
    )
    approved_date_eng = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Approved Date (Eng)",
        help_text="स्वीकृत मिति (अंग्रेजी)",
    )


class ProjectAddress(BaseModel):
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Municipality",
        help_text="नगरपालिका",
    )
    ward = models.CharField(
        max_length=55, null=True, blank=True, verbose_name="Ward", help_text="वडा"
    )
    ward_eng = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Ward (Eng)",
        help_text="वडा (अंग्रेजी)",
    )
    house_no = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="House No",
        help_text="घर नं",
    )
    tole = models.CharField(
        max_length=55, null=True, blank=True, verbose_name="Tole", help_text="टोल"
    )
    tole_eng = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Tole (Eng)",
        help_text="टोल (अंग्रेजी)",
    )
    road_name_eng = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Road Name (Eng)",
        help_text="सडकको नाम (अंग्रेजी)",
    )
    road_name = models.ForeignKey(
        Road,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Road",
        help_text="सडकको नाम",
    )
    village_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Village Name",
        help_text="गाउँको नाम",
    )


class WorkProject(CommonFieldsBase):
    name = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Name",
        help_text="योजनाको नाम",
    )
    name_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Name (Eng)",
        help_text="योजनाको नाम (अंग्रेजी)",
    )
    work_class = models.ForeignKey(
        WorkClass,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Work Class",
        help_text="कामको वर्ग",
    )
    work_type = models.ForeignKey(
        ProjectWorkType,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text="कामको प्रकार",
    )
    proposed_type = models.ForeignKey(
        ProjectProposedType,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Proposed Type",
        help_text="योजनाको प्रस्ताबित प्रकार",
    )
    user_committee = models.ForeignKey(
        ConsumerCommittee,
        null=True,
        on_delete=models.PROTECT,
        blank=True,
        verbose_name="User Committee",
        help_text=" उपभोक्ता समिति",
    )
    ward = models.IntegerField(
        null=True, blank=True, verbose_name="Ward No.", help_text="वडा नं. "
    )
    proposed_financial_year = models.ForeignKey(
        FinancialYear,
        null=True,
        blank=True,
        related_name="proposed_fy",
        on_delete=models.PROTECT,
        verbose_name="Proposed Financial Year",
        help_text="प्रस्तावित आर्थिक बर्ष ",
    )
    financial_year = models.ForeignKey(
        FinancialYear,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="financial_year",
        verbose_name="Financial Year",
        help_text="आर्थिक बर्ष ",
    )
    proposed_unit_type = models.ForeignKey(
        Unit,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="proposed_unit_type",
        help_text="प्रस्थाबित योजना/कार्यक्रम को प्रकार",
    )
    proposed_project_outcome = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Proposed Project Outcome",
        help_text="प्रस्थाबित योजना/कार्यक्रमको परिणाम",
    )
    address = models.ForeignKey(
        Address,
        null=True,
        blank=True,
        related_name="work_projects",
        on_delete=models.PROTECT,
        verbose_name="Address",
        help_text="ठेगाना",
    )
    project_address = models.ForeignKey(
        ProjectAddress,
        null=True,
        blank=True,
        related_name="work_projects",
        on_delete=models.PROTECT,
        verbose_name="Address",
        help_text="ठेगाना",
    )
    # project_level = models.CharField(
    #     max_length=50, choices=PROJECT_LEVEL, default="local_level"
    # )
    project_level = models.ForeignKey(
        ProjectLevel,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Project Level",
        help_text="योजनाको स्तर",
    )
    proposed_date = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Proposed Date",
        help_text="प्रस्तावित मिति",
    )
    proposed_date_eng = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Proposed Date (Eng)",
        help_text="प्रस्तावित मिति (अंग्रेजी)",
    )
    estimated_start_date = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Estimated Start Date",
        help_text="अनुमानित सुरु मिति",
    )
    estimated_start_date_eng = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Estimated Start Date (Eng)",
        help_text="अनुमानित सुरु मिति (अंग्रेजी)",
    )
    estimated_end_date = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Estimated End Date",
        help_text="अनुमानित समापन मिति",
    )
    estimated_end_date_eng = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Estimated End Date (Eng)",
        help_text="अनुमानित समापन मिति (अंग्रेजी)",
    )
    estimated_amount = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Estimated Amount",
        help_text="अनुमानित रकम",
    )
    internal_source = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Internal Source",
        help_text="आन्तरिक स्रोत",
    )
    nepal_gov = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Nepal Government",
        help_text="नेपाल सरकार",
    )
    province_gov = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Province Government",
        help_text="प्रदेश सरकार",
    )
    local_level_gov = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Local Level Government",
        help_text="स्थानीय तह",
    )
    loan = models.CharField(
        max_length=40, null=True, blank=True, verbose_name="Loan", help_text="कर्जा"
    )
    public_participation = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Public Participation",
        help_text="सार्वजनिक सहभागिता",
    )
    benefited_households = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Benefited Households",
        help_text="लाभान्वित घरधुरीहरु",
    )
    benefited_population = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Benefited Population",
        help_text="लाभान्वित जनसंख्या",
    )
    achievement = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="Achievement",
        help_text="अधिगम",
    )
    approve = models.ForeignKey(
        ApproveProcess,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Approve Process",
        help_text="अनुमोदन प्रक्रिया",
    )
    is_prioritized = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="Is Prioritized",
        help_text="प्राथमिकतामा राखिएको छ",
    )
    project_prioritization = models.ForeignKey(
        PriorityType,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Project Prioritization",
        help_text="प्राथमिकताको प्रकार",
    )
    priority_approved_by = models.ForeignKey(
        Employee,
        related_name="priority_approved_by",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Priority Approved By",
        help_text="प्राथमिकता स्वीकृत गर्ने",
    )
    priority_approved_date = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Priority Approved Date",
        help_text="प्राथमिकता स्वीकृत मिति",
    )
    priority_approved_date_eng = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Priority Approved Date (Eng)",
        help_text="प्राथमिकता स्वीकृत मिति (अंग्रेजी)",
    )
    budget_assurance = models.ForeignKey(
        BudgetAssurance,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Budget Assurance",
        help_text="बजेट आश्वासन",
    )
    project_approved_date = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Project Approved Date",
        help_text="योजना स्वीकृत मिति",
    )
    project_approved_date_eng = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Project Approved Date (Eng)",
        help_text="योजना स्वीकृत मिति (अंग्रेजी)",
    )
    project_approved_by = models.ForeignKey(
        Employee,
        related_name="project_approved_by",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Project Approved By",
        help_text="योजना स्वीकृत गर्ने",
    )
    is_approved = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="Is Approved",
        help_text="स्वीकृत गरिएको छ",
    )
    approved_date = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Approved Date",
        help_text="स्वीकृत मिति",
    )
    approved_date_eng = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Approved Date (Eng)",
        help_text="स्वीकृत मिति (अंग्रेजी)",
    )
    remarks = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Remarks",
        help_text="कैफियत",
    )
    kramagat = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Kramagat",
        help_text="क्रमागत",
    )

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectDocument(BaseModel):
    project = models.ForeignKey(
        WorkProject, on_delete=models.PROTECT, null=True, blank=True
    )
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.PROTECT, null=True, blank=True
    )
    report_type = models.ForeignKey(
        "project_report.ReportType",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Report Type",
        help_text="प्रतिवेदनको प्रकार",
    )
    document_file = models.FileField(upload_to="uploads/project_documents/")
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.document_type.document_type if self.document_type else str(self.id)
