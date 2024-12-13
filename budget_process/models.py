from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from base_model.models import Address, CommonFieldsBase
from employee.models import Employee
from project.models import BaseModel, FinancialYear, Project
from project_planning.models import (
    AccountTitleManagement,
    BudgetSource,
    SubjectArea,
    SubModule,
)
from utils.constants import ALLOCATION_TYPE, EXPENSE_DETERMINE_LEVEL

# Create your models here.


# व्यय बजेट सिमा निर्धारण


class Source(BaseModel):
    internal_source = models.BigIntegerField(null=True, blank=True)
    nepal_gov = models.BigIntegerField(null=True, blank=True)
    province_gov = models.BigIntegerField(null=True, blank=True)
    local_gov = models.BigIntegerField(null=True, blank=True)
    loan = models.BigIntegerField(null=True, blank=True)
    public_participation = models.BigIntegerField(blank=True, null=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class ApproveProcess(BaseModel):
    is_prepared = models.BooleanField(
        default=False, verbose_name="Prepared", help_text="तयार भयो"
    )
    is_verified = models.BooleanField(
        default=False, verbose_name="Verified", help_text="प्रमाणित गरियो"
    )
    is_approved = models.BooleanField(
        default=False, verbose_name="Approved", help_text="स्वीकृत गरियो"
    )
    prepared_by = models.ForeignKey(
        Employee,
        related_name="p_employee",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Prepared By",
        help_text="द्वारा तयार",
    )
    prepared_date = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Prepared Date",
        help_text="तयार मिति",
    )
    prepared_date_eng = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Prepared Date (Eng)",
        help_text="तयार मिति (अंग्रेजी)",
    )
    verified_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="v_employee",
        null=True,
        blank=True,
        verbose_name="Verified By",
        help_text="द्वारा प्रमाणित",
    )
    verified_date = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Verified Date",
        help_text="प्रमाणित मिति",
    )
    verified_date_eng = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Verified Date (Eng)",
        help_text="प्रमाणित मिति (अंग्रेजी)",
    )
    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="a_employee",
        null=True,
        blank=True,
        verbose_name="Approved By",
        help_text="द्वारा स्वीकृत",
    )
    approved_date = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Approved Date",
        help_text="स्वीकृत मिति",
    )
    approved_date_eng = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Approved Date (Eng)",
        help_text="स्वीकृत मिति (अंग्रेजी)",
    )

    def __str__(self):
        return str(self.id)


class IncomeExpenseDetermine(CommonFieldsBase):
    financial_year = models.ForeignKey(
        FinancialYear, null=True, blank=True, on_delete=models.PROTECT
    )
    estimated_amount = models.BigIntegerField(null=True, blank=True)
    date = models.CharField(max_length=100, null=True, blank=True)
    date_eng = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        abstract = True


class ExpenseBudgetRangeDetermine(IncomeExpenseDetermine):
    expense_determine_level = models.CharField(
        max_length=15, choices=EXPENSE_DETERMINE_LEVEL
    )
    ward = models.IntegerField(null=True, blank=True)
    expense_title_no = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)
    source_type = models.ForeignKey(
        Source, blank=True, null=True, on_delete=models.PROTECT
    )
    approve_process = models.ForeignKey(
        ApproveProcess,
        related_name="approve_process_ebrd",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    is_budget_estimates = models.BooleanField(default=False)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.expense_title_no)

    # def __str__(self):
    #     return f"ExpenseBudgetRangeDetermine(id={self.id}, ward={self.ward}, is_budget_estimates={self.is_budget_estimates})"

    @property
    def internal_source(self):
        return self.source_type.internal_source

    @property
    def is_approved(self):
        return self.approve_process.is_approved


class IncomeBudgetRangeDetermine(IncomeExpenseDetermine):
    income_title_no = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)
    source_type = models.ForeignKey(
        Source, blank=True, null=True, on_delete=models.PROTECT
    )
    approve_process = models.ForeignKey(
        ApproveProcess,
        blank=True,
        related_name="approve_process_ibrd",
        null=True,
        on_delete=models.PROTECT,
    )
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def internal_source(self):
        return self.source_type.internal_source

    @property
    def is_approved(self):
        return self.approve_process.is_approved


class EstimateFinancialArrangements(IncomeExpenseDetermine):
    income_title_no = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)
    approve_process = models.ForeignKey(
        ApproveProcess,
        blank=True,
        related_name="approve_process_efa",
        null=True,
        on_delete=models.PROTECT,
    )
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def is_approved(self):
        return self.approve_process.is_approved


class BudgetExpenseManagement(BaseModel):
    expense_title_number = models.CharField(max_length=55, null=True, blank=True)
    municipality = models.ForeignKey(
        "project.Municipality",
        null=True,
        blank=True,
        related_name="budget_expenses",
        on_delete=models.PROTECT,
    )
    expense_title = models.ForeignKey(
        "project_planning.AccountTitleManagement",
        null=True,
        blank=True,
        related_name="budget_expenses",
        on_delete=models.PROTECT,
    )
    sub_module = models.ForeignKey(
        SubModule,
        blank=True,
        null=True,
        related_name="budget_expenses",
        on_delete=models.PROTECT,
    )
    budget_source = models.ForeignKey(
        BudgetSource,
        blank=True,
        null=True,
        related_name="budget_expenses",
        on_delete=models.PROTECT,
    )
    financial_year = models.ForeignKey(
        FinancialYear, blank=True, null=True, on_delete=models.PROTECT
    )
    revised_sub_module = models.ForeignKey(
        SubModule,
        blank=True,
        null=True,
        related_name="revised_budget_expenses",
        on_delete=models.PROTECT,
    )
    revised_expense_amount = models.BigIntegerField(null=True, blank=True)
    revision_reason = models.CharField(max_length=255, null=True, blank=True)
    revised_financial_year = models.ForeignKey(
        FinancialYear,
        blank=True,
        null=True,
        related_name="revised_budget_expenses",
        on_delete=models.PROTECT,
    )
    first_quarter = models.BigIntegerField(null=True, blank=True)
    second_quarter = models.BigIntegerField(null=True, blank=True)
    third_quarter = models.BigIntegerField(null=True, blank=True)
    forth_quarter = models.BigIntegerField(null=True, blank=True)
    estimated_expense_amount = models.BigIntegerField(null=True, blank=True)
    subject_area = models.ForeignKey(
        SubjectArea, blank=True, null=True, on_delete=models.PROTECT
    )
    activity_name = models.CharField(max_length=500, blank=True, null=True)
    aim = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=500, blank=True, null=True)
    approval_process = models.ForeignKey(
        ApproveProcess, null=True, blank=True, on_delete=models.PROTECT
    )
    status = models.BooleanField(default=True, null=True, blank=True)


class BudgetTransfer(BaseModel):
    transfer_date = models.CharField(max_length=50, null=True, blank=True)
    transfer_date_eng = models.CharField(max_length=50, null=True, blank=True)
    total_amount = models.BigIntegerField(null=True, blank=True)
    display_order = models.BigIntegerField(null=True, blank=True)
    allocation_id = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class BudgetManagement(BaseModel):
    acc_id = models.IntegerField(null=True, blank=True)
    value = models.BigIntegerField(null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class BudgetAmmendment(BaseModel):
    """बजेट संशोधनको विवरण"""

    sub_module = models.ForeignKey(
        SubModule, blank=True, null=True, on_delete=models.PROTECT
    )
    budget_source = models.ForeignKey(
        BudgetSource, blank=True, null=True, on_delete=models.PROTECT
    )
    financial_year = models.ForeignKey(
        FinancialYear, blank=True, null=True, on_delete=models.PROTECT
    )
    from_year = models.CharField(max_length=50, null=True, blank=True)
    from_year_eng = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    kramagat = models.IntegerField(null=True, blank=True)
    account_title = models.ForeignKey(
        AccountTitleManagement, on_delete=models.PROTECT, null=True, blank=True
    )

    allocation_type = models.CharField(
        max_length=15, choices=ALLOCATION_TYPE, null=True, blank=True
    )
    budget_management = models.ForeignKey(
        BudgetManagement,
        help_text="बजेट व्यवस्थापन",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    rakam = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class BudgetImportLog(BaseModel):
    """बजेट आयात लग विवरण"""

    imported_file = models.FileField(upload_to="budget_import_logs")
    import_payload = models.JSONField()
    import_status = models.BooleanField(default=False)
    imported_bem = models.ManyToManyField(
        BudgetExpenseManagement,
        blank=True,
        related_name="import_log",
    )
    imported_projects = models.ManyToManyField(
        Project,
        blank=True,
        related_name="import_log",
    )
    imported_budget_allocation_details = models.ManyToManyField(
        "plan_execution.BudgetAllocationDetail",
        blank=True,
        related_name="import_log",
    )
    imported_addresses = models.ManyToManyField(
        Address,
        blank=True,
        related_name="import_log",
    )
    imported_project_executions = models.ManyToManyField(
        "plan_execution.ProjectExecution",
        blank=True,
        related_name="import_log",
    )
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)


# Signals
@receiver(post_save, sender=BudgetExpenseManagement)
def create_project(sender, instance, created, **kwargs):
    from plan_execution.models import BudgetAllocationDetail, ProjectExecution

    # TODO: Make it update when data is updated.
    if created:
        import_log = instance.import_log.first()
        project = Project.objects.create(
            municipality=instance.municipality,
            name=instance.activity_name,
            financial_year=instance.financial_year,
        )
        address = Address.objects.create(
            municipality=instance.municipality,
        )
        project_execution = ProjectExecution.objects.create(
            project=project,
            address=address,
            appropriated_amount=instance.estimated_expense_amount,
            subject_area=instance.subject_area,
            financial_year=instance.financial_year,
            name=instance.activity_name,
        )
        budget_allocation_detail = BudgetAllocationDetail.objects.create(
            project=project_execution,
            expense_title=instance.expense_title,
            subject_area=instance.subject_area,
            budget_source=instance.budget_source,
            first_quarter=instance.first_quarter,
            second_quarter=instance.second_quarter,
            third_quarter=instance.third_quarter,
            fourth_quarter=instance.forth_quarter,
            total=instance.estimated_expense_amount,
        )
        if import_log:
            import_log.imported_projects.add(project)
            import_log.imported_project_executions.add(project_execution)
            import_log.imported_budget_allocation_details.add(budget_allocation_detail)
            import_log.imported_addresses.add(address)
