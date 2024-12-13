import datetime
import locale

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from base_model.models import Address, CommonFieldsBase
from employee.models import Department, Employee, EmployeeSector, Position
from formulate_plan.models import WorkClass, WorkProject
from plan_execution.choices import (
    BOQTypeChoices,
    CommentSentForChoices,
    CommentStatusChoices,
    PaymentTypes,
    ProcessNameChoices,
)
from project.models import BaseModel, Project, Unit
from project_planning.models import (
    BFI,
    AccountTitleManagement,
    BudgetSource,
    BudgetSubTitle,
    ConstructionMaterialDescription,
    ConsumerCommittee,
    ExpanseType,
    MemberType,
    MonitoringCommittee,
    MonitoringCommitteeMember,
    NewsPaper,
    Organization,
    PaymentMedium,
    PriorityType,
    Program,
    ProjectActivity,
    ProjectLevel,
    ProjectNature,
    ProjectStartDecision,
    ProjectType,
    PurposePlan,
    SelectionFeasibility,
    SourceReceipt,
    StrategicSign,
    SubjectArea,
    TargetGroup,
)
from project_report.models import ReportType
from user.models import User
from utils.constants import (
    BAIL_TYPES,
    BANK_GUARANTEE_TYPE,
    MANDATE_TYPE,
    PROJECT_PHASES,
    PROJECT_STATUSES,
    STATUS_CHOICES,
    WORK_PROPOSER_TYPE,
    ProcessStatus,
    RequestSend,
)
from utils.nepali_date import bs_to_ad
from utils.nepali_nums import english_nums

# Create your models here.


class StartPmsProcess(CommonFieldsBase):
    def __str__(self):
        return f"{self.code} - {self.name}"


class PlanStartDecision(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectExecution(WorkProject):
    project = models.OneToOneField(
        Project,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Project",
        help_text="योजना",
    )
    phase = models.CharField(
        max_length=50,
        choices=PROJECT_PHASES,
        default="created",
        verbose_name="Phase",
        help_text="अवस्था",
    )
    project_type = models.ForeignKey(
        ProjectType,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="project_executions",
        verbose_name="Project Type",
        help_text="योजना प्रकार",
    )
    project_nature = models.ForeignKey(
        ProjectNature,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Project Nature",
        help_text="योजना प्रकृति",
    )
    purpose = models.ForeignKey(
        PurposePlan,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Purpose",
        help_text="उद्देश्य",
    )
    subject_area = models.ForeignKey(
        SubjectArea,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Subject Area",
        related_name="sa_execution",
        help_text="विषयगत कार्यक्षेत्र",
    )
    work_area = models.ForeignKey(
        SubjectArea,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Work Area",
        related_name="wa_execution",
        help_text="कार्यक्षेत्र",
    )
    strategic_sign = models.ForeignKey(
        StrategicSign,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Strategic Sign",
        help_text="रणनीतिक चिन्ह",
    )
    work_proposer_type = models.CharField(
        choices=WORK_PROPOSER_TYPE,
        null=True,
        blank=True,
        max_length=55,
        verbose_name="Work Proposer Type",
        help_text="कार्य प्रस्तावक प्रकार",
    )

    program = models.ForeignKey(
        Program,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Program",
        help_text="कार्यक्रम",
    )
    project_priority = models.ForeignKey(
        PriorityType,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Project Priority",
        help_text="योजना प्राथमिकता",
    )
    start_pms_process = models.ForeignKey(
        StartPmsProcess,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Operating Procedures",
        help_text="सञ्चालन प्रकृया",
    )
    plan_start_decision = models.ForeignKey(
        PlanStartDecision,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Plan Start Decision",
        help_text="योजना सुरु गर्ने निर्णय",
    )
    # लक्ष्य परिमाण SECTION
    first_trimester = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="First Trimester",
        help_text="प्रथम त्रैमासिक",
    )
    second_trimester = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Second Trimester",
        help_text="दोस्रो त्रैमासिक",
    )
    third_trimester = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Third Trimester",
        help_text="तेस्रो त्रैमासिक",
    )
    fourth_trimester = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Fourth Trimester",
        help_text="चौथो त्रैमासिक",
    )
    is_multi_year_plan = models.BooleanField(
        default=False, verbose_name="Multi Year Plan", help_text="बहु वर्षीय योजना"
    )
    first_year = models.BigIntegerField(
        null=True, blank=True, verbose_name="First Year", help_text="प्रथम वर्ष"
    )
    second_year = models.BigIntegerField(
        null=True, blank=True, verbose_name="Second Year", help_text="दोस्रो वर्ष"
    )
    third_year = models.BigIntegerField(
        null=True, blank=True, verbose_name="Third Year", help_text="तेस्रो वर्ष"
    )
    forth_year = models.BigIntegerField(
        null=True, blank=True, verbose_name="Fourth Year", help_text="चौथो वर्ष"
    )
    fifth_year = models.BigIntegerField(
        null=True, blank=True, verbose_name="Fifth Year", help_text="पाँचौ वर्ष"
    )
    # लाभान्वितको विवरण

    other = models.BigIntegerField(
        null=True, blank=True, verbose_name="Other", help_text="अन्य"
    )
    #     total_committee_members
    # total_gathered_organizations

    total_committee_members = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Total Committee Members",
        help_text="जम्मा समुदाय संख्या",
    )

    total_gathered_organizations = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Total Gathered Organizations",
        help_text="जम्मा संगठित संस्था संख्या",
    )

    latitude = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Latitude",
        help_text="अक्षांश",
    )
    longitude = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Longitude",
        help_text="देशान्तर",
    )
    appropriated_amount = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Appropriated Amount",
        help_text="अवस्थित रकम",
    )
    overhead = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Overhead",
        help_text="ओभरहेड",
    )
    contingency = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Contingency",
        help_text="आकस्मिक",
    )
    contingency_percent = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Contingency Percent",
        help_text="आकस्मिक प्रतिशत",
    )
    mu_aa_ka = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Mu Aa Ka",
        help_text="मु आ क",
    )
    mu_aa_ka_percent = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Mu Aa Ka Percent",
        help_text="मु आ क प्रतिशत",
    )
    public_charity = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Public Charity",
        help_text="सार्वजनिक दान",
    )
    public_charity_percent = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Public Charity Percent",
        help_text="सार्वजनिक दान प्रतिशत",
    )
    maintenance = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Maintenance",
        help_text="रखरखाव",
    )
    maintenance_percent = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Maintenance Percent",
        help_text="रखरखाव प्रतिशत",
    )
    disaster_mgmt_fund = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Disaster Management Fund",
        help_text="प्रकोप व्यवस्थापन कोष",
    )
    disaster_mgmt_fund_percent = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Disaster Management Fund Percent",
        help_text="प्रकोप व्यवस्थापन कोष प्रतिशत",
    )
    total_estimate = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Total Estimate",
        help_text="कुल अनुमान",
    )
    self_payment = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Self Payment",
        help_text="स्वयं भुक्तानी",
    )
    is_executing = models.BooleanField(
        default=True, verbose_name="Executing", help_text="कार्यान्वयन गर्दै"
    )
    subtotal_estimate = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Subtotal Estimate",
        help_text="उपयोगकर्ता अनुमान",
    )

    @property
    def agreement(self):
        return (
            self.openingcontractaccount_set.first() or self.projectagreement_set.first()
        )

    @property
    def deadline_date(self) -> datetime.date | None:
        return self.agreement.deadline if self.agreement else None

    @property
    def is_completed(self):
        return self.project_work_finish.exists() or self.ups_project_complete.exists()

    @property
    def project_status(self):
        if self.is_completed:
            return PROJECT_STATUSES[3]
        elif self.paymentexitbill_set.filter(installment__code="first").exists():
            return PROJECT_STATUSES[2]
        elif (
            self.openingcontractaccount_set.exists()
            and self.openingcontractaccount_set.first().is_agreement_done
        ):
            return PROJECT_STATUSES[1]
        else:
            return PROJECT_STATUSES[0]

    @property
    def is_delayed(self):
        return not self.is_completed

    @property
    def is_ongoing(self):
        return not self.is_completed and not self.is_delayed

    @property
    def total_benefitted_houses(self):
        if self.project_benefited_detail.exists():
            return self.project_benefited_detail.aggregate(
                total_benefitted_houses=models.Sum("total_house_number")
            )["total_benefitted_houses"]
        return 0

    @property
    def total_benefitted_male_population(self):
        if self.project_benefited_detail.exists():
            return self.project_benefited_detail.aggregate(
                total_benefitted_male_population=models.Sum("total_man")
            )["total_benefitted_male_population"]
        return 0

    @property
    def total_benefitted_female_population(self):
        if self.project_benefited_detail.exists():
            return self.project_benefited_detail.aggregate(
                total_benefitted_female_population=models.Sum("total_women")
            )["total_benefitted_female_population"]
        return 0

    @property
    def total_benefitted_other_population(self):
        if self.project_benefited_detail.exists():
            return self.project_benefited_detail.aggregate(
                total_benefitted_other_population=models.Sum("total_other")
            )["total_benefitted_other_population"]
        return 0

    @property
    def total_benefitted_population(self):
        if self.project_benefited_detail.exists():
            return self.project_benefited_detail.aggregate(
                total_benefitted_population=models.Sum("total_population")
            )["total_benefitted_population"]
        return 0

    @property
    def selected_consumer_committee(self):
        if self.project_consumer_formulation.exists():
            consumer_formulation = (
                self.project_consumer_formulation.all().order_by("id").first()
            )
            if consumer_formulation:
                return (
                    consumer_formulation.selected_consumer_committee
                    or consumer_formulation.consumer_committee
                )
        return None


class ProjectPhysicalDescription(CommonFieldsBase):
    unit_type = models.ForeignKey(
        Unit,
        related_name="project_unit_type",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        ProjectExecution,
        related_name="project_physical_detail",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    remarks = models.CharField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectExecutionDocument(CommonFieldsBase):
    project = models.ForeignKey(
        ProjectExecution,
        related_name="project_execution_document",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=120, null=True, blank=True)
    doc_type = models.CharField(max_length=120, null=True, blank=True)
    doc_size = models.CharField(max_length=120, null=True, blank=True)
    document = models.FileField(upload_to="project_execution/")
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectUnitDetail(BaseModel):
    unit_type = models.ForeignKey(
        Unit,
        related_name="project_unit_detail",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        ProjectExecution,
        related_name="project_unit",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    unit = models.FloatField(null=True, blank=True)
    unit_rate = models.FloatField(null=True, blank=True)
    total_unit = models.FloatField(null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class BudgetAllocationDetail(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        related_name="project_budget_allocation_detail",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    budget_sub_title = models.ForeignKey(
        BudgetSubTitle, null=True, blank=True, on_delete=models.PROTECT
    )
    expense_title = models.ForeignKey(
        AccountTitleManagement,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="allocated_budget_details",
    )
    subject_area = models.ForeignKey(
        SubjectArea, null=True, blank=True, on_delete=models.PROTECT
    )
    program = models.ForeignKey(
        Program, null=True, blank=True, on_delete=models.PROTECT
    )
    budget_source = models.ForeignKey(
        BudgetSource, null=True, blank=True, on_delete=models.PROTECT
    )
    source_receipt = models.ForeignKey(
        SourceReceipt, null=True, blank=True, on_delete=models.PROTECT
    )
    expense_method = models.ForeignKey(
        PaymentMedium, null=True, blank=True, on_delete=models.PROTECT
    )
    first_quarter = models.BigIntegerField(null=True, blank=True)
    second_quarter = models.BigIntegerField(null=True, blank=True)
    third_quarter = models.BigIntegerField(null=True, blank=True)
    fourth_quarter = models.BigIntegerField(null=True, blank=True)
    total = models.BigIntegerField(null=True, blank=True)
    multi_year_budget = models.BooleanField(default=False)
    is_revise_budget = models.BooleanField(default=False)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class BenefitedDetail(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        related_name="project_benefited_detail",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    target_group = models.ForeignKey(
        TargetGroup, null=True, blank=True, on_delete=models.PROTECT
    )
    total_house_number = models.IntegerField(null=True, blank=True)
    total_man = models.IntegerField(null=True, blank=True)
    total_women = models.IntegerField(null=True, blank=True)
    total_other = models.IntegerField(null=True, blank=True)
    total_population = models.IntegerField(null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class ProjectTask(BaseModel):
    project = models.ForeignKey(ProjectExecution, on_delete=models.CASCADE)
    task = models.CharField(max_length=200, null=True, blank=True)
    task_status = models.CharField(
        max_length=200, choices=STATUS_CHOICES, default="सुचारु नभएको"
    )
    weight = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)


# PROJECT SIDE DATA


class TenderPurchaseBranch(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class BailType(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class AccountingTopic(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectInstallment(CommonFieldsBase):
    start_pms_process = models.ManyToManyField(
        StartPmsProcess,
        blank=True,
        verbose_name="Operating Procedures",
        help_text="सञ्चालन प्रकृया",
    )

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ExpenseTypeDetail(BaseModel):
    expense_type = models.ForeignKey(
        ExpanseType, null=True, blank=True, on_delete=models.PROTECT
    )
    amount = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class EstimationSubmitAcceptance(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        related_name="project_estimation_as",
        on_delete=models.CASCADE,
    )
    is_estimate_submitted = models.BooleanField(default=False)
    estimated_by = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        related_name="project_estimated_by",
        on_delete=models.CASCADE,
    )
    estimated_by_post = models.ForeignKey(
        EmployeeSector,
        null=True,
        blank=True,
        related_name="project_estimated_by_post",
        on_delete=models.CASCADE,
    )
    estimate_date = models.CharField(max_length=50, null=True, blank=True)
    estimate_date_eng = models.CharField(max_length=50, null=True, blank=True)
    is_cited = models.BooleanField(default=False)
    cited_by = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        related_name="project_cited_by",
        on_delete=models.CASCADE,
    )
    cited_by_post = models.ForeignKey(
        EmployeeSector,
        null=True,
        blank=True,
        related_name="project_cited_by_post",
        on_delete=models.CASCADE,
    )
    cited_date = models.CharField(max_length=50, null=True, blank=True)
    cited_date_eng = models.CharField(max_length=50, null=True, blank=True)
    is_recommended = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        related_name="project_recommended_by",
        on_delete=models.CASCADE,
    )
    recommended_by_post = models.ForeignKey(
        EmployeeSector,
        null=True,
        blank=True,
        related_name="project_recommended_by_post",
        on_delete=models.CASCADE,
    )
    recommended_date = models.CharField(max_length=50, null=True, blank=True)
    recommended_date_eng = models.CharField(max_length=50, null=True, blank=True)
    is_accounting_opinion_submitted = models.BooleanField(default=False)
    accounting_opinion_submitted_by = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        related_name="project_accounting_opinion_submitted_by",
        on_delete=models.CASCADE,
    )
    accounting_opinion_submitted_by_post = models.ForeignKey(
        EmployeeSector,
        null=True,
        blank=True,
        related_name="project_accounting_opinion_submitted_by_post",
        on_delete=models.CASCADE,
    )
    accounting_opinion_submitted_date = models.CharField(
        max_length=50, null=True, blank=True
    )
    accounting_opinion_submitted_date_eng = models.CharField(
        max_length=50, null=True, blank=True
    )
    accounting_opinion = models.CharField(max_length=150, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        related_name="project_esa_approved_by",
        on_delete=models.CASCADE,
    )
    approved_by_post = models.ForeignKey(
        EmployeeSector,
        null=True,
        blank=True,
        related_name="project_esa_post",
        on_delete=models.CASCADE,
    )
    approved_date = models.CharField(max_length=50, null=True, blank=True)
    approved_date_eng = models.CharField(max_length=50, null=True, blank=True)
    approve_opinion = models.CharField(max_length=150, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class ProjectTender(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        related_name="project_tender",
        on_delete=models.CASCADE,
    )
    first_published_date = models.CharField(max_length=50, null=True, blank=True)
    first_published_date_eng = models.CharField(max_length=50, null=True, blank=True)
    bids_purchase_last_date = models.CharField(max_length=50, null=True, blank=True)
    bids_purchase_last_date_eng = models.CharField(max_length=50, null=True, blank=True)
    bids_purchase_time = models.CharField(max_length=50, null=True, blank=True)
    bids_enrollment_last_date = models.CharField(max_length=50, null=True, blank=True)
    bids_enrollment_last_date_eng = models.CharField(
        max_length=50, null=True, blank=True
    )
    bids_enrollment_time = models.CharField(max_length=50, null=True, blank=True)
    bids_open_date = models.CharField(max_length=50, null=True, blank=True)
    bids_open_date_eng = models.CharField(max_length=50, null=True, blank=True)
    bids_open_time = models.CharField(max_length=50, null=True, blank=True)
    bids_purchase_branch = models.ForeignKey(
        Department,
        related_name="pt_bpb_branch",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    bids_enrollment_branch = models.ForeignKey(
        Department,
        related_name="pt_beb_branch",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    contact_branch = models.ForeignKey(
        Department,
        related_name="pt_cb_branch",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    invoice_date = models.CharField(max_length=50, null=True, blank=True)
    invoice_date_eng = models.CharField(max_length=50, null=True, blank=True)
    invoice_no = models.CharField(max_length=50, null=True, blank=True)
    new_paper_name = models.ForeignKey(
        NewsPaper, null=True, blank=True, on_delete=models.PROTECT
    )
    news_paper_address = models.CharField(max_length=50, null=True, blank=True)
    printing_press = models.CharField(max_length=50, null=True, blank=True)
    paper_page_no = models.CharField(max_length=100, null=True, blank=True)
    info_publication_no = models.CharField(max_length=100, null=True, blank=True)
    info_publication_price = models.CharField(max_length=50, null=True, blank=True)
    publication_date = models.CharField(max_length=50, null=True, blank=True)
    publication_date_eng = models.CharField(max_length=50, null=True, blank=True)
    voucher_date = models.CharField(max_length=50, null=True, blank=True)
    voucher_date_eng = models.CharField(max_length=50, null=True, blank=True)
    voucher_no = models.CharField(max_length=50, null=True, blank=True)
    address1 = models.TextField(null=True, blank=True)
    address2 = models.TextField(null=True, blank=True)
    address3 = models.TextField(null=True, blank=True)
    address4 = models.TextField(null=True, blank=True)
    address5 = models.TextField(null=True, blank=True)
    address6 = models.TextField(null=True, blank=True)
    representative_invoice_date = models.CharField(max_length=50, null=True, blank=True)
    representative_invoice_date_eng = models.CharField(
        max_length=50, null=True, blank=True
    )
    representative_invoice_no = models.CharField(max_length=50, null=True, blank=True)
    representative_send_date = models.CharField(max_length=50, null=True, blank=True)
    representative_send_time = models.CharField(max_length=50, null=True, blank=True)
    representative_send_address = models.CharField(max_length=50, null=True, blank=True)
    representative1 = models.TextField(null=True, blank=True)
    representative2 = models.TextField(null=True, blank=True)
    representative3 = models.TextField(null=True, blank=True)
    representative4 = models.TextField(null=True, blank=True)
    representative5 = models.TextField(null=True, blank=True)
    representative6 = models.TextField(null=True, blank=True)
    print_custom_report = models.BooleanField(default=False)
    status = models.BooleanField(default=True, null=True, blank=True)


class ProjectBidCollection(BaseModel):
    project = models.ForeignKey(
        ProjectExecution, null=True, blank=True, on_delete=models.PROTECT
    )
    builder = models.ForeignKey(
        Organization, null=True, blank=True, on_delete=models.PROTECT
    )
    is_legal = models.BooleanField(default=False)
    bail_type = models.CharField(
        BAIL_TYPES, max_length=50, null=True, blank=True, default="बैल"
    )
    bail_amount = models.CharField(max_length=50, null=True, blank=True)
    bank = models.ForeignKey(BFI, null=True, blank=True, on_delete=models.PROTECT)
    bank_guarantee_type = models.CharField(
        choices=BANK_GUARANTEE_TYPE, max_length=50, null=True, blank=True
    )
    bank_guarantee_no = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.CharField(max_length=50, null=True, blank=True)
    start_date_eng = models.CharField(max_length=50, null=True, blank=True)
    end_date = models.CharField(max_length=50, null=True, blank=True)
    end_date_eng = models.CharField(max_length=50, null=True, blank=True)
    total_amount = models.CharField(max_length=50, null=True, blank=True)
    mu_aa_ka = models.CharField(max_length=50, null=True, blank=True)
    total = models.CharField(max_length=50, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    attached_documents_list = models.CharField(max_length=155255, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    @property
    def builder_name(self):
        return self.builder.name if self.builder else None

    @property
    def builder_pan_no(self):
        return self.builder.pan_number if self.builder else None


class ProjectDarbhauBid(BaseModel):
    project = models.ForeignKey(
        ProjectExecution, null=True, blank=True, on_delete=models.PROTECT
    )
    bid_sale_no = models.CharField(max_length=50, null=True, blank=True)
    bid_enrollment_no = models.CharField(max_length=50, null=True, blank=True)
    legal_bid = models.CharField(max_length=50, null=True, blank=True)
    comment_date = models.CharField(max_length=50, null=True, blank=True)
    comment_date_eng = models.CharField(max_length=50, null=True, blank=True)
    comment_no = models.CharField(max_length=50, null=True, blank=True)
    comment_approved_date = models.CharField(max_length=50, null=True, blank=True)
    comment_approved_date_eng = models.CharField(max_length=50, null=True, blank=True)
    position = models.ForeignKey(
        EmployeeSector, blank=True, null=True, on_delete=models.PROTECT
    )
    approved_by = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.PROTECT
    )
    firm = models.ForeignKey(
        Organization, blank=True, null=True, on_delete=models.PROTECT
    )
    proprietor_name = models.TextField(blank=True, null=True)
    submitter_opinion = models.TextField(blank=True, null=True)
    accountant_opinion = models.TextField(blank=True, null=True)
    project_head_opinion = models.TextField(blank=True, null=True)
    office_head_decision = models.TextField(blank=True, null=True)
    executive_decision = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class ProjectAgreement(BaseModel):
    project = models.ForeignKey(
        ProjectExecution, null=True, blank=True, on_delete=models.CASCADE
    )
    contractor_invoiced_no = models.CharField(max_length=50, null=True, blank=True)
    contractor_invoiced_date = models.CharField(max_length=50, null=True, blank=True)
    contractor_invoiced_date_eng = models.CharField(
        max_length=50, null=True, blank=True
    )
    contractor_remarks_1 = models.CharField(max_length=50, null=True, blank=True)
    contractor_remarks_2 = models.CharField(max_length=50, null=True, blank=True)
    required_bail_amount = models.CharField(max_length=50, null=True, blank=True)
    required_performance_bond_amount = models.CharField(
        max_length=50, null=True, blank=True
    )
    required_bail_date = models.CharField(null=True, blank=True, max_length=50)
    required_bail_date_eng = models.CharField(null=True, blank=True, max_length=50)
    firm_name = models.ForeignKey(
        Organization, null=True, blank=True, on_delete=models.PROTECT
    )
    firm_address = models.CharField(max_length=150, null=True, blank=True)
    firm_contact_no = models.CharField(max_length=50, null=True, blank=True)
    grand_father_name = models.CharField(max_length=50, null=True, blank=True)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    contracting_party_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    contract_date = models.CharField(max_length=100, null=True, blank=True)
    contract_date_eng = models.CharField(max_length=100, null=True, blank=True)
    work_finished_date = models.CharField(max_length=50, null=True, blank=True)
    work_finished_date_eng = models.CharField(max_length=50, null=True, blank=True)
    exist_bail_amount = models.CharField(max_length=50, null=True, blank=True)
    exist_performance_bond_amount = models.CharField(
        max_length=50, null=True, blank=True
    )
    bank = models.ForeignKey(BFI, null=True, blank=True, on_delete=models.PROTECT)
    exist_bank_guarantee_no = models.CharField(max_length=50, null=True, blank=True)
    exist_bail_date = models.CharField(null=True, blank=True, max_length=50)
    exist_bail_date_eng = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(max_length=50, null=True, blank=True)
    end_date_eng = models.CharField(max_length=50, null=True, blank=True)
    contractors_witness = models.CharField(max_length=50, null=True, blank=True)
    cw_position = models.ForeignKey(
        Position,
        related_name="project_cwp",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    office_witness_1 = models.ForeignKey(
        Employee,
        related_name="employee_w1",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    office_witness_1_position = models.ForeignKey(
        "employee.EmployeeSector",
        related_name="project_ow1",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    office_witness_2 = models.ForeignKey(
        Employee,
        related_name="employee_w2",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    office_witness_2_position = models.ForeignKey(
        "employee.EmployeeSector",
        related_name="project_ow2",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    office_witness_3 = models.ForeignKey(
        Employee,
        related_name="employee_w3",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    office_witness_3_position = models.ForeignKey(
        "employee.EmployeeSector",
        related_name="project_ow3",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    office_witness_4 = models.ForeignKey(
        Employee,
        related_name="employee_w4",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    office_witness_4_position = models.ForeignKey(
        "employee.EmployeeSector",
        related_name="project_ow4",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    mandate_invoice_no = models.CharField(max_length=50, null=True, blank=True)
    mandate_invoice_date = models.CharField(max_length=50, null=True, blank=True)
    mandate_invoice_date_eng = models.CharField(max_length=50, null=True, blank=True)
    pa_sa = models.CharField(max_length=50, null=True, blank=True)
    remark_1 = models.CharField(max_length=50, null=True, blank=True)
    remark_2 = models.CharField(max_length=50, null=True, blank=True)
    remark_3 = models.CharField(max_length=50, null=True, blank=True)
    remark_4 = models.CharField(max_length=50, null=True, blank=True)
    officer_name = models.CharField(max_length=50, null=True, blank=True)
    officer_position = models.CharField(max_length=50, null=True, blank=True)
    print_custom_name = models.BooleanField(default=False)
    status = models.BooleanField(default=True, null=True, blank=True)

    @property
    def is_agreement_done(self):
        return self.contract_date is not None

    @property
    def deadline(self):
        return bs_to_ad(self.work_finished_date) if self.work_finished_date else None


class ProjectMobilization(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Project Execution",
        help_text="योजना कार्यान्वयन",
    )
    comment_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Comment No.",
        help_text="टिप्पणी नं.",
    )
    project_amount = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Project Amount",
        help_text="योजना रकम",
    )
    date = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Date",
        help_text="मिति",
    )
    percent = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Percent",
        help_text="प्रतिशत",
    )
    date_eng = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Date (AD)",
        help_text="मिति (इ.स.)",
    )
    mobilization_amount = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Mobilization Amount",
        help_text="योजना संचालन रकम",
    )
    address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Address",
        help_text="ठेगाना",
    )
    remarks = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Remarks",
        help_text="कैफियत",
    )
    print_custom_report = models.BooleanField(
        default=False,
        verbose_name="Print Custom Report",
        help_text="कस्टम रिपोर्ट प्रिन्ट गर्नुहोस्",
    )


class ProjectMobilizationDetail(BaseModel):
    mobilization = models.ForeignKey(
        ProjectMobilization,
        on_delete=models.CASCADE,
        related_name="mobilization_details",
        verbose_name="Project Mobilization",
        help_text="योजना संचालन",
    )
    institution = models.ForeignKey(
        SourceReceipt,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Body",
        help_text="निकाय",
    )
    accounting_topic = models.ForeignKey(
        AccountTitleManagement,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Accounting Topic",
        help_text="लेखा शीर्षक",
    )
    budget_source = models.ForeignKey(
        BudgetSource,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Budget Source",
        help_text="बजेट स्रोत",
    )
    percentage = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Percent",
        help_text="प्रतिशत",
    )
    amount = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Amount",
        help_text="रकम",
    )
    remarks = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Remarks",
        help_text="कैफियत",
    )


class PaymentDetail(BaseModel):
    expense_topic = models.ForeignKey(
        AccountTitleManagement,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Expense Topic",
        help_text="खर्च शीर्षक",
    )
    source = models.ForeignKey(
        SourceReceipt,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Source",
        help_text="श्रोत",
    )
    subject_work_area = models.ForeignKey(
        SubjectArea,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Subject Work Area",
        help_text="विषय क्षेत्र",
    )
    payment_type = models.ForeignKey(
        "project_planning.CollectPayment",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Type",
        help_text="प्रकार",
    )
    amount = models.BigIntegerField(
        null=True, blank=True, verbose_name="Amount", help_text="रकम"
    )
    remarks = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Remarks",
        help_text="कैफियत",
    )
    peb = models.ForeignKey(
        "PaymentExitBill",
        null=True,
        blank=True,
        related_name="payment_details",
        on_delete=models.PROTECT,
        verbose_name="Payment Exit Bill",
        help_text="भुक्तानी निस्कने बिल",
    )


class PaymentExitBill(BaseModel):
    project = models.ForeignKey(
        ProjectExecution, null=True, blank=True, on_delete=models.CASCADE
    )
    letter_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Letter No.",
        help_text="पत्र नं.",
    )
    cha_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Invoice No.",
        help_text="चलानी नं.",
    )
    exit_date = models.CharField(max_length=50, null=True, blank=True)
    exit_date_eng = models.CharField(max_length=50, null=True, blank=True)
    installment = models.ForeignKey(
        ProjectInstallment,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="peb",
    )
    payment_mode = models.CharField(
        max_length=5,
        null=True,
        blank=True,
        choices=PaymentTypes.choices,
        verbose_name="Payment Type",
        help_text="भुक्तानी प्रकार",
    )
    u_sa_maag_amount = models.BigIntegerField(null=True, blank=True)
    check_pass_date = models.CharField(max_length=50, null=True, blank=True)
    check_pass_date_eng = models.CharField(max_length=50, null=True, blank=True)
    check_pass_name = models.ForeignKey(
        Employee, null=True, blank=True, on_delete=models.PROTECT
    )
    check_pass_position = models.ForeignKey(
        EmployeeSector, null=True, blank=True, on_delete=models.PROTECT
    )
    disbursement_assessment_amount = models.BigIntegerField(null=True, blank=True)
    check_pass_amount = models.BigIntegerField(null=True, blank=True)
    contentment_amount = models.BigIntegerField(null=True, blank=True)
    mu_aa_ka = models.BigIntegerField(null=True, blank=True)
    marmat_sambhar_fund_amount = models.BigIntegerField(null=True, blank=True)
    env_disaster_fund_amount = models.BigIntegerField(null=True, blank=True)
    public_participation_percent = models.BigIntegerField(null=True, blank=True)
    public_participation_amount = models.BigIntegerField(null=True, blank=True)
    reinstatement_tex = models.BigIntegerField(null=True, blank=True)
    advance_income_tex = models.BigIntegerField(null=True, blank=True)
    withdrawal_eligible_amount = models.BigIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    plan_mst_total_amount = models.BigIntegerField(null=True, blank=True)
    peski_amount = models.BigIntegerField(null=True, blank=True)
    nikasha_total_amount = models.BigIntegerField(null=True, blank=True)
    total_remaining_amount = models.BigIntegerField(null=True, blank=True)
    ready_by = models.ForeignKey(
        Employee,
        related_name="peb_ready_emp",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    ready_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="peb_ready_position",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    submitted_by = models.ForeignKey(
        Employee,
        related_name="peb_submit_emp",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    submitted_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="peb_submit_position",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    approved_by = models.ForeignKey(
        Employee,
        related_name="peb_approve_emp",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    approved_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="peb_approve_position",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    status = models.BooleanField(default=True, null=True, blank=True)

    @property
    def total_from_payment_details(self) -> int:
        return self.payment_details.aggregate(models.Sum("amount"))["amount__sum"] or 0

    @staticmethod
    def previous_installment_code(installment_code) -> str | None:
        installment_codes_list = ["first", "second", "third", "fourth", "last"]
        previous_installment_code_index = (
            installment_codes_list.index(installment_code) - 1
        )
        if previous_installment_code_index < 0:
            return None
        return installment_codes_list[previous_installment_code_index]

    @property
    def previous_installment_peski_amount(self):
        previous_installment_code = self.previous_installment_code(
            self.installment.code
        )
        if previous_installment_code:
            previous_installment = self.project.paymentexitbill_set.filter(
                installment__code=previous_installment_code
            ).first()
            if previous_installment:
                return previous_installment.peski_amount
        return 0

    def save(self, *args, **kwargs):
        if self.status:
            self.plan_mst_total_amount = int(english_nums(self.project.self_payment))
            self.nikasha_total_amount = self.total_from_payment_details
            self.peski_amount = (
                self.previous_installment_peski_amount + self.nikasha_total_amount
            )
            self.total_remaining_amount = self.plan_mst_total_amount - self.peski_amount
        super().save(*args, **kwargs)


class ProjectDeadline(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="extensions",
    )
    cha_no = models.CharField(max_length=50, null=True, blank=True)
    letter_no = models.CharField(max_length=50, null=True, blank=True)
    deadline_date = models.CharField(max_length=50, null=True, blank=True)
    deadline_date_eng = models.CharField(max_length=50, null=True, blank=True)
    decision_date = models.CharField(max_length=50, null=True, blank=True)
    decision_date_eng = models.CharField(max_length=50, null=True, blank=True)
    decision_by = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="deadline_extensions_decided",
    )
    site_inspector = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="deadline_sites_inspected",
    )
    site_inspector_position = models.ForeignKey(
        EmployeeSector,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="deadline_sites_inspected",
    )
    site_inspection_date = models.CharField(max_length=50, null=True, blank=True)
    reason = models.CharField(max_length=250, null=True, blank=True)
    remark = models.CharField(max_length=150, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class MeasuringBook(BaseModel):
    project = models.ForeignKey(
        ProjectExecution, null=True, blank=True, on_delete=models.CASCADE
    )
    measuring_no = models.CharField(max_length=100, null=True, blank=True)
    activity = models.ForeignKey(
        ProjectActivity, blank=True, null=True, on_delete=models.PROTECT
    )
    page_no = models.CharField(max_length=100, null=True, blank=True)
    measuring_date = models.CharField(max_length=100, null=True, blank=True)
    measuring_date_eng = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.CharField(max_length=100, null=True, blank=True)
    previous_measuring_book_amount = models.BigIntegerField(null=True, blank=True)
    this_measuring_book_amount = models.BigIntegerField(null=True, blank=True)
    result_obtained_so_far = models.BigIntegerField(null=True, blank=True)
    rate_in_list = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    breath = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    contractor = models.ForeignKey(
        Organization, blank=True, null=True, on_delete=models.PROTECT
    )
    contractor_position = models.ForeignKey(
        EmployeeSector,
        related_name="cp_position",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    measured_by = models.ForeignKey(
        Employee,
        related_name="mb_measured_emp",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    measured_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="mb_position",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    checked_by = models.ForeignKey(
        Employee,
        related_name="mb_checked_emp",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    checked_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="mb_cb_position",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    approved_by = models.ForeignKey(
        Employee,
        related_name="mb_approved_emp",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    approved_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="mb_ab_position",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    status = models.BooleanField(default=True, null=True, blank=True)


class ProjectFinishedBailReturn(BaseModel):
    """
    Theka paththa bata yojana sampanna bhayeko
    """

    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="project_work_finish",
    )
    comment_no = models.CharField(max_length=100, blank=True, null=True)
    date = models.CharField(max_length=100, null=True, blank=True)
    date_eng = models.CharField(max_length=100, null=True, blank=True)
    executive_decision = models.CharField(max_length=100, null=True, blank=True)
    approved_by = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.PROTECT
    )
    approved_by_position = models.ForeignKey(
        EmployeeSector, blank=True, null=True, on_delete=models.PROTECT
    )
    print_custom_report = models.BooleanField(default=False)
    status = models.BooleanField(default=True, null=True, blank=True)


# उपभोक्ता छनौट/गठन


class ConsumerFormulation(BaseModel):
    """
    Consumer Committee Formulation
    """

    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="project_consumer_formulation",
        verbose_name="Project Execution",
        help_text="योजना कार्यान्वयन",
    )
    print_custom_report = models.BooleanField(
        default=False,
        verbose_name="Custom Report Print",
        help_text="कस्टम रिपोर्ट प्रिन्ट गर्नुहोस्",
    )
    first_time_publish = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="First Published Date",
        help_text="पहिलो पटक प्रकाशित मिति",
    )
    first_time_publish_eng = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="First Published Date (AD)",
        help_text="पहिलो पटक प्रकाशित मिति (AD)",
    )
    form_amount = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Form Amount",
        help_text="फारम दस्तुर रकम",
    )
    consumer_committee = models.ForeignKey(
        ConsumerCommittee,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Consumer Committee",
        help_text="उपभोक्ता समिति",
    )
    consumer_committee_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Consumer Committee Name",
        help_text="उपभोक्ता समिति नाम",
    )
    selected_consumer_committee = models.ForeignKey(
        ConsumerCommittee,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="selected_consumer_committee",
        verbose_name="Selected Consumer Committee",
        help_text="छनौट गरिएको उपभोक्ता समिति",
    )
    code = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Code", help_text="कोड"
    )
    chairman = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Chairman",
        help_text="अध्यक्ष",
    )
    address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Address",
        help_text="ठेगाना",
    )
    established_date = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Established Date",
        help_text="स्थापना मिति",
    )
    phone = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Phone", help_text="फोन"
    )
    report_date = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Report Date",
        help_text="प्रतिवेदन मिति",
    )
    report_date_eng = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Report Date (AD)",
        help_text="प्रतिवेदन मिति (AD)",
    )
    invoice_no = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Invoice No",
        help_text="बिल नं",
    )
    project_current_status = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Project Current Status",
        help_text="योजना चालु अवस्था",
    )
    previous_work = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Previous Work",
        help_text="अघिल्लो कार्य",
    )
    detail_from_office_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Detail From Office Date",
        help_text="कार्यालयबाट विवरण मिति",
    )
    detail_from_office_date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Detail From Office Date (AD)",
        help_text="कार्यालयबाट विवरण मिति (AD)",
    )
    office_lecture = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Office Lecture",
        help_text="कार्यालय बैठक",
    )
    emp_name = models.ForeignKey(
        Employee,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Employee",
        help_text="कर्मचारी",
    )
    monitoring_committee = models.ForeignKey(
        MonitoringCommittee,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Monitoring Committee",
        help_text="निर्वाह समिति",
    )
    monitor_committee = models.ManyToManyField(
        MonitoringCommitteeMember,
        blank=True,
        related_name="formulation",
        verbose_name="Monitoring Committee Member",
        help_text="निर्वाह समिति सदस्य",
    )
    position = models.ForeignKey(
        EmployeeSector,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="EmployeeSector",
        help_text="पद",
    )
    opinion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Opinion",
        help_text="अभिप्राय",
    )
    positive_effect = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Positive Effect",
        help_text="सकारात्मक प्रभाव",
    )
    other = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Other", help_text="अन्य"
    )
    project_related_other = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Project Related Other",
        help_text="योजना सम्बन्धी अन्य",
    )

    @property
    def cc(self):
        return self.selected_consumer_committee or self.consumer_committee


class PSABuildingMaterial(BaseModel):
    material = models.ForeignKey(
        ConstructionMaterialDescription,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Material",
        help_text="सामग्री",
    )
    amount = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Amount", help_text="परिमाण"
    )
    rupees = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Rupees",
        help_text="रुपैयाँ",
    )
    remark = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Remark", help_text="कैफियत"
    )
    probability_study_approve = models.ForeignKey(
        "ProbabilityStudyApprove",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="materials",
        verbose_name="Probability Study Approve",
        help_text="सम्भाव्यता अध्ययन/स्वीकृत",
    )


class ProbabilityStudyApprove(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Project Execution",
        help_text="योजना कार्यान्वयन",
    )
    project_selection = models.ForeignKey(
        SelectionFeasibility,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Project Selection",
        help_text="योजना छनौट",
    )
    consumer_benefits = models.TextField(
        null=True,
        blank=True,
        verbose_name="Consumer Benefits",
        help_text="उपभोक्ता लाभ",
    )
    engineer_survey_to_start_future = models.TextField(
        null=True,
        blank=True,
        verbose_name="Engineer Survey To Start Future",
        help_text="अभियन्ता सर्वेक्षण भविष्यमा सुरु गर्ने",
    )
    recommender_opinion = models.TextField(
        null=True,
        blank=True,
        verbose_name="Recommender's Opinion",
        help_text="सिफारिसको अभिप्राय",
    )
    approvers_opinion = models.TextField(
        null=True,
        blank=True,
        verbose_name="Approver's Opinion",
        help_text="अनुमोदनको अभिप्राय",
    )
    approved_amount_percent = models.CharField(
        null=True,
        blank=True,
        verbose_name="Approved Amount Percent",
        help_text="अनुमोदित रकम प्रतिशत",
    )
    decision = models.TextField(
        null=True,
        blank=True,
        verbose_name="Decision",
        help_text="निर्णय",
    )
    submission_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Submission Date",
        help_text="पेश गर्ने मिति",
    )
    submission_date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Submission Date (AD)",
        help_text="पेश गर्ने मिति (AD)",
    )
    submission_date_by = models.ForeignKey(
        Employee,
        related_name="emp_submission_date_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Submission By",
        help_text="पेश गर्ने",
    )
    submission_date_by_position = models.ForeignKey(
        EmployeeSector,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Submitter's Position",
        help_text="पेश गर्नेको पद",
    )
    check_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Check Date",
        help_text="जाँच मिति",
    )
    check_date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Check Date (AD)",
        help_text="जाँच मिति (AD)",
    )
    check_by = models.ForeignKey(
        Employee,
        related_name="emp_check_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Check By",
        help_text="जाँच गर्ने",
    )
    check_date_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="check_date_by_position_emp",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Checker's Position",
        help_text="जाँच गर्नेको पद",
    )
    recommendation_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Recommendation Date",
        help_text="सिफारिस मिति",
    )
    recommendation_date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Recommendation Date (AD)",
        help_text="सिफारिस मिति (AD)",
    )
    recommendation_by = models.ForeignKey(
        Employee,
        related_name="emp_recommendation_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Recommendation By",
        help_text="सिफारिस गर्ने",
    )
    recommendation_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="recommendation_by_position_emp",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Recommender's Position",
        help_text="सिफारिस गर्नेको पद",
    )
    approved_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Approved Date",
        help_text="अनुमोदन मिति",
    )
    approved_date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Approved Date (AD)",
        help_text="अनुमोदन मिति (AD)",
    )
    approved_by = models.ForeignKey(
        Employee,
        related_name="emp_approved_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Approved By",
        help_text="अनुमोदन गर्ने",
    )
    approved_date_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="approved_date_by_position_emp",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Approver's Position",
        help_text="अनुमोदन गर्नेको पद",
    )
    to_approve_submission_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Submission Date Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी पेश गर्ने मिति",
    )
    to_approve_submission_date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Submission Date Regarding Project Approval and Agreement (AD)",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी पेश गर्ने मिति (AD)",
    )
    to_approve_submission_by = models.ForeignKey(
        Employee,
        related_name="emp_to_approve_submission_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Submission By Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी पेश गर्ने",
    )
    to_approve_submission_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="to_approve_submission_by_position_emp",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Submitter's Position Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी पेश गर्नेको पद",
    )
    to_approve_check_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Check Date Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी जाँच गर्ने मिति",
    )
    to_approve_check_date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Check Date Regarding Project Approval and Agreement (AD)",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी जाँच गर्ने मिति (AD)",
    )
    to_approve_check_by = models.ForeignKey(
        Employee,
        related_name="emp_to_approve_check_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Checker Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी जाँच गर्ने",
    )
    to_approve_check_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="to_approve_check_by_position_emp",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Checker's Position Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी जाँच गर्नेको पद",
    )
    to_approve_recommendation_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Recommendation Date Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी सिफारिस मिति",
    )
    to_approve_recommendation_date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Recommendation Date Regarding Project Approval and Agreement (AD)",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी सिफारिस मिति (AD)",
    )
    to_approve_recommendation_by = models.ForeignKey(
        Employee,
        related_name="emp_to_approve_recommendation_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Recommendation By Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी सिफारिस गर्ने",
    )
    to_approve_recommendation_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="to_approve_recommendation_by_position_emp",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Recommender's Position Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी सिफारिस गर्नेको पद",
    )
    to_approve_approved_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Approved Date Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी अनुमोदन मिति",
    )
    to_approve_approved_date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Approved Date Regarding Project Approval and Agreement (AD)",
        help_text="आयोजना स्वीकृत तथा सम्झौता सम्बन्धी अनुमोदन मिति (AD)",
    )
    to_approve_approved_by = models.ForeignKey(
        Employee,
        related_name="emp_to_approve_approved_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Approved By Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता अनुमोदन गर्ने",
    )
    to_approve_approved_by_position = models.ForeignKey(
        EmployeeSector,
        related_name="to_approve_approved_by_position_emp",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Approver's Position Regarding Project Approval and Agreement",
        help_text="आयोजना स्वीकृत तथा सम्झौता अनुमोदन गर्नेको पद",
    )
    invoice_no = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Invoice No",
        help_text="बिल नं",
    )
    label = models.TextField(
        null=True, blank=True, verbose_name="Label", help_text="लेबल"
    )
    pa_na = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Pa No.", help_text="प. नं"
    )
    final_report_approved_by = models.ForeignKey(
        Employee,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="final_report_approved_by_emp",
        verbose_name="Final Report Approved By",
        help_text="अन्तिम प्रतिवेदन अनुमोदन गर्ने",
    )


# सम्झौता खाता खोलिदिने
class InstallmentDetail(BaseModel):
    installment = models.ForeignKey(
        ProjectInstallment,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Installment",
        help_text="किस्ता",
    )
    date = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Date", help_text="मिति"
    )
    date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Date (AD)",
        help_text="मिति (AD)",
    )
    nikasha_total_amount = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Amount", help_text="रकम"
    )
    public_participation_percent = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Percent",
        help_text="प्रतिशत",
    )
    remark = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Remark", help_text="कैफियत"
    )
    opening_contract_account = models.ForeignKey(
        "OpeningContractAccount",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="installment",
        verbose_name="Opening Contract Account",
        help_text="सम्झौता खाता खोलिदिने",
    )


class BuildingMaterialDetail(BaseModel):
    source = models.ForeignKey(
        BudgetSource,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Source",
        help_text="स्रोत",
    )
    material = models.ForeignKey(
        ConstructionMaterialDescription,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Material",
        help_text="सामग्री",
    )
    amount = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Amount", help_text="परिमाण"
    )
    remark = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Remark", help_text="कैफियत"
    )
    opening_contract_account = models.ForeignKey(
        "OpeningContractAccount",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="materials",
        verbose_name="Opening Contract Account",
        help_text="सम्झौता खाता खोलिदिने",
    )


class MaintenanceArrangement(BaseModel):
    source = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Source", help_text="स्रोत"
    )
    amount = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Amount", help_text="रकम"
    )
    remark = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Remark", help_text="कैफियत"
    )
    opening_contract_account = models.ForeignKey(
        "OpeningContractAccount",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="maintenance",
        verbose_name="Opening Contract Account",
        help_text="सम्झौता खाता खोलिदिने",
    )


class OpeningContractAccount(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Project Execution",
        help_text="योजना कार्यान्वयन",
    )
    cha_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Chalani No.",
        help_text="चलानी नं",
    )
    pa_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Pa No.",
        help_text="प नं",
    )
    date = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Date",
        help_text="मिति",
    )
    date_eng = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Date (AD)",
        help_text="मिति (AD)",
    )
    bank_name = models.ForeignKey(
        BFI,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Bank/Financial Institution",
        help_text="बैंक/वित्तीय संस्था",
    )
    account_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Account No.",
        help_text="खाता नं",
    )
    bank_branch = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Bank Branch",
        help_text="बैंक शाखा",
    )
    bodarth = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Bodarth",
        help_text="बोधार्थ",
    )
    contract_ch_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Contract Chalani No.",
        help_text="सम्झौता चलानी नं",
    )
    contract_date = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Contract Date",
        help_text="सम्झौता मिति",
    )
    contract_pa_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Contract Pa No.",
        help_text="सम्झौता प नं",
    )
    bodarth_1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Bodarth 1",
        help_text="बोधार्थ १",
    )
    bodarth_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Bodarth 2",
        help_text="बोधार्थ २",
    )
    day = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Day", help_text="दिन"
    )
    contract_account_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Contract Account No.",
        help_text="सम्झौता खाता नं",
    )
    print_custom_report = models.BooleanField(
        default=False,
        verbose_name="Custom Report Print",
        help_text="कस्टम रिपोर्ट प्रिन्ट गर्नुहोस्",
    )
    project_contract_date = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Project Contract Date",
        help_text="योजना सम्झौता मिति",
    )
    project_contract_date_eng = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Project Contract Date (AD)",
        help_text="योजना सम्झौता मिति (AD)",
    )
    project_contract_start_date = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Project Contract Start Date",
        help_text="योजना सम्झौता सुरु मिति",
    )
    project_contract_start_date_eng = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Project Contract Start Date (AD)",
        help_text="योजना सम्झौता सुरु मिति (AD)",
    )
    project_completion_date = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Project Completion Date",
        help_text="योजना सम्पन्न मिति",
    )
    project_completion_date_eng = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Project Completion Date (AD)",
        help_text="योजना सम्पन्न मिति (AD)",
    )
    contract_no = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Contract No.",
        help_text="सम्झौता नं",
    )
    present_benefit = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Present Benefit",
        help_text="उपस्थित लाभ",
    )
    absent_benefit = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Absent Benefit",
        help_text="अनुपस्थित लाभ",
    )
    project_start_experience = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Project Start Experience",
        help_text="योजना सुरु अनुभव",
    )
    other_experience = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Other Experience",
        help_text="अन्य अनुभव",
    )
    cost_participation_subsidy = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name="Cost Participation Subsidy",
        help_text="खर्च भागिदारी अनुदान",
    )
    public_service_labour_force = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name="Public Service Labour Force",
        help_text="सार्वजनिक सेवा श्रम बल",
    )
    arrangements_for_taking_care_of_repairs = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Arrangements For Taking Care Of Repairs",
        help_text="मरम्मत गर्ने व्यवस्था",
    )
    repairs_by_company = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Repairs By Company",
        help_text="कम्पनीले मरम्मत गर्ने",
    )
    committee_witness = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Committee Witness",
        help_text="समितिको साक्षी",
    )
    witness_consumer_committee_post = models.ForeignKey(
        "project_planning.ConsumerCommitteeMember",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="oca_witness",
        verbose_name="Witness Consumer Committee Post",
        help_text="साक्षी उपभोक्ता समिति पद",
    )
    user_committee_secretary = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="User Committee Secretary",
        help_text="उपभोक्ता समिति सचिव",
    )
    secretary_of_consumer_committee_post = models.ForeignKey(
        "project_planning.ConsumerCommitteeMember",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="oca_secretary",
        verbose_name="Secretary of Consumer Committee Post",
        help_text="उपभोक्ता समिति सचिव पद",
    )
    office_side_1 = models.ForeignKey(
        Employee,
        related_name="office_side_1_emp",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="First Employee on Behalf of Office",
        help_text="कार्यालयको तर्फबाट पहिलो कर्मचारी",
    )
    office_side_1_position = models.ForeignKey(
        EmployeeSector,
        related_name="office_side_1_position",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="First Employee's Position on Behalf of Office",
        help_text="कार्यालयको तर्फबाट पहिलो कर्मचारीको पद",
    )
    office_side_2 = models.ForeignKey(
        Employee,
        related_name="office_side_2_emp",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Second Employee on Behalf of Office",
        help_text="कार्यालयको तर्फबाट दोस्रो कर्मचारी",
    )
    office_side_2_position = models.ForeignKey(
        EmployeeSector,
        related_name="office_side_2_position",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Second Employee's Position on Behalf of Office",
        help_text="कार्यालयको तर्फबाट दोस्रो कर्मचारीको पद",
    )
    office_side_3 = models.ForeignKey(
        Employee,
        related_name="office_side_3_emp",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Third Employee on Behalf of Office",
        help_text="कार्यालयको तर्फबाट तेस्रो कर्मचारी",
    )
    office_side_3_position = models.ForeignKey(
        EmployeeSector,
        related_name="office_side_3_position",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Third Employee's Position on Behalf of Office",
        help_text="कार्यालयको तर्फबाट तेस्रो कर्मचारीको पद",
    )
    office_side_4 = models.ForeignKey(
        Employee,
        related_name="office_side_4_emp",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Fourth Employee on Behalf of Office",
        help_text="कार्यालयको तर्फबाट चौथो कर्मचारी",
    )
    office_side_4_position = models.ForeignKey(
        EmployeeSector,
        related_name="office_side_4_position",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Fourth Employee's Position on Behalf of Office",
        help_text="कार्यालयको तर्फबाट चौथो कर्मचारीको पद",
    )
    mandate_ch_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Mandate Chalani No.",
        help_text="बिधेयक चलानी नं",
    )
    mandate_date = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Mandate Date",
        help_text="बिधेयक मिति",
    )
    mandate_date_eng = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Mandate Date (AD)",
        help_text="बिधेयक मिति (AD)",
    )
    mandate_pa_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Mandate Pa No.",
        help_text="बिधेयक प नं",
    )
    mandate_bodarth = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Mandate Bodarth",
        help_text="बिधेयक बोधार्थ",
    )
    mandate_employee = models.ForeignKey(
        Employee,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="mandate_employee",
        verbose_name="Mandate Employee",
        help_text="बिधेयक कर्मचारी",
    )
    mandate_employee_position = models.ForeignKey(
        EmployeeSector,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="mandate_employee_position",
        verbose_name="Mandate Employee's Position",
        help_text="बिधेयक कर्मचारीको पद",
    )
    ward_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Ward No.",
        help_text="वडा नं",
    )

    @property
    def is_agreement_done(self):
        return self.contract_date is not None

    @property
    def deadline(self):
        return (
            bs_to_ad(self.project_completion_date)
            if self.project_completion_date
            else None
        )


class MonitoringCommitteeDetail(BaseModel):
    member_type = models.ForeignKey(
        MemberType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Member Type",
        help_text="सदस्य प्रकार",
    )
    member_position = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Member Position",
        help_text="सदस्य पद",
    )
    member_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Member Name",
        help_text="सदस्यको नाम",
    )
    phone_no = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Phone No.",
        help_text="फोन नं",
    )
    present = models.BooleanField(
        default=False, verbose_name="Present", help_text="उपस्थित"
    )


class UserCommitteeMonitoring(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Project Execution",
        help_text="योजना कार्यान्वयन",
    )
    project_amount = models.BigIntegerField(
        null=True, blank=True, verbose_name="Project Amount", help_text="योजना रकम"
    )
    assessment_amount = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Assessment Amount",
        help_text="मूल्यांकन रकम",
    )
    amount_payable_as_per_assessment = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Amount Payable As Per Assessment",
        help_text="मूल्यांकन अनुसार भुक्तानी गर्नु पर्ने रकम",
    )
    date = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Date", help_text="मिति"
    )
    date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Date (AD)",
        help_text="मिति (AD)",
    )
    meeting_address = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Meeting Address",
        help_text="बैठकको ठेगाना",
    )
    proposal_1 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Proposal 1",
        help_text="प्रस्ताव १",
    )
    proposal_2 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Proposal 2",
        help_text="प्रस्ताव २",
    )
    proposal_3 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Proposal 3",
        help_text="प्रस्ताव ३",
    )
    print_custom_report = models.BooleanField(
        default=False,
        verbose_name="Custom Report Print",
        help_text="कस्टम रिपोर्ट प्रिन्ट गर्नुहोस्",
    )

    @property
    def is_done(self):
        return not (
            self.date is None
            or self.proposal_1 is None
            or self.proposal_2 is None
            or self.proposal_3 is None
        )


class ProjectRevision(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Project Execution",
        help_text="योजना कार्यान्वयन",
    )
    revision_date = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Revision Date",
        help_text="संशोधन मिति",
    )
    revision_date_eng = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Revision Date (AD)",
        help_text="संशोधन मिति (AD)",
    )
    process_start_ward = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Process Start Ward",
        help_text="प्रक्रिया सुरु वडा",
    )
    project_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Project Name",
        help_text="योजना नाम",
    )
    project_name_eng = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Project Name (Eng)",
        help_text="योजना नाम (Eng)",
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Address",
        help_text="ठेगाना",
    )

    project_level = models.ForeignKey(
        ProjectLevel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Project Level",
        help_text="योजना स्तर",
    )
    project_type = models.ForeignKey(
        ProjectType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Project Type",
        help_text="योजना प्रकार",
    )
    project_nature = models.ForeignKey(
        ProjectNature,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Project Nature",
        help_text="योजना स्वभाव",
    )
    work_class = models.ForeignKey(
        WorkClass,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Work Class",
        help_text="कार्य वर्ग",
    )
    subject_area = models.ForeignKey(
        SubjectArea,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Subject Area",
        help_text="विषय क्षेत्र",
    )
    strategic_sign = models.ForeignKey(
        StrategicSign,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Strategic Sign",
        help_text="रणनीतिक चिन्ह",
    )
    work_proposer_type = models.CharField(
        choices=WORK_PROPOSER_TYPE,
        null=True,
        blank=True,
        max_length=55,
        verbose_name="Work Proposer Type",
        help_text="कार्य प्रस्तावक प्रकार",
    )
    priority_type = models.ForeignKey(
        PriorityType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Priority Type",
        help_text="प्राथमिकता प्रकार",
    )
    project_start_decision = models.ForeignKey(
        ProjectStartDecision,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Project Start Decision",
        help_text="योजना सुरु निर्णय",
    )

    # लक्ष्य परिमाण SECTION
    first_trimester = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="First Trimester",
        help_text="प्रथम त्रैमासिक",
    )
    second_trimester = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Second Trimester",
        help_text="दोस्रो त्रैमासिक",
    )
    third_trimester = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Third Trimester",
        help_text="तेस्रो त्रैमासिक",
    )
    fourth_trimester = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Fourth Trimester",
        help_text="चौथो त्रैमासिक",
    )
    is_multi_year_plan = models.BooleanField(
        default=False,
        verbose_name="Is Multi Year Plan",
        help_text="बहु वर्षीय योजना हो",
    )
    first_year = models.BigIntegerField(
        null=True, blank=True, verbose_name="First Year", help_text="पहिलो वर्ष"
    )
    second_year = models.BigIntegerField(
        null=True, blank=True, verbose_name="Second Year", help_text="दोस्रो वर्ष"
    )
    third_year = models.BigIntegerField(
        null=True, blank=True, verbose_name="Third Year", help_text="तेस्रो वर्ष"
    )
    forth_year = models.BigIntegerField(
        null=True, blank=True, verbose_name="Forth Year", help_text="चौथो वर्ष"
    )
    fifth_year = models.BigIntegerField(
        null=True, blank=True, verbose_name="Fifth Year", help_text="पाँचौ वर्ष"
    )
    # लाभान्वितको विवरण
    other = models.BigIntegerField(
        null=True, blank=True, verbose_name="Other", help_text="अन्य"
    )
    latitude = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Latitude",
        help_text="अक्षांश",
    )
    longitude = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Longitude",
        help_text="देशान्तर",
    )

    appropriated_amount = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Appropriated Amount",
        help_text="अवस्थित रकम",
    )
    overhead = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Overhead",
        help_text="ओभरहेड",
    )
    contingency = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Contingency",
        help_text="आकस्मिक",
    )
    contingency_percent = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Contingency Percent",
        help_text="आकस्मिक प्रतिशत",
    )
    mu_aa_ka = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Mu Aa Ka",
        help_text="मु आ क",
    )
    mu_aa_ka_percent = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Mu Aa Ka Percent",
        help_text="मु आ क प्रतिशत",
    )
    public_charity = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Public Charity",
        help_text="सार्वजनिक चारिटी",
    )
    public_charity_percent = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Public Charity Percent",
        help_text="सार्वजनिक चारिटी प्रतिशत",
    )
    maintenance = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Maintenance Fund",
        help_text="मर्मत सम्भार कोष",
    )
    maintenance_percent = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Maintenance Percent",
        help_text="मर्मत सम्भार कोष प्रतिशत",
    )
    disaster_mgmt_fund = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Environment and Disaster Management Fund",
        help_text="पर्यावरण तथा विपद् प्रबन्धन कोष",
    )
    total_estimate = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Total Cost Estimate",
        help_text="कुल लागत अनुमान",
    )
    self_payment = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Self Payment",
        help_text="स्वयं भुक्तानी",
    )
    remarks = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Remarks",
        help_text="कैफियत",
    )
    karmagat = models.IntegerField(
        null=True, blank=True, verbose_name="Karmagat", help_text="कर्मगत"
    )

    def __str__(self):
        return str(self.id)


class UserCommitteeDocuments(BaseModel):
    document_file = models.FileField(upload_to="user_committee_docs/")
    document_name = models.CharField(max_length=120, blank=True, null=True)
    document_size = models.CharField(max_length=30, blank=True, null=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class UserCommitteeProjectWorkComplete(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="ups_project_complete",
    )
    ch_no = models.CharField(max_length=100, null=True, blank=True)
    pa_no = models.CharField(max_length=100, null=True, blank=True)
    project_complete_date = models.CharField(max_length=100, null=True, blank=True)
    project_complete_date_eng = models.CharField(max_length=100, null=True, blank=True)
    bank = models.ForeignKey(BFI, on_delete=models.PROTECT, null=True, blank=True)
    account_no = models.CharField(max_length=100, null=True, blank=True)
    submitted_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ucp_submitted_by",
    )
    submitted_by_position = models.ForeignKey(
        EmployeeSector,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ucp_submitted_by_position",
    )
    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ucp_approved_by",
    )
    approved_by_position = models.ForeignKey(
        EmployeeSector,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ucp_approved_by_position",
    )
    bodarth = models.CharField(max_length=100, null=True, blank=True)
    print_custom_report = models.BooleanField(default=False)
    # project_document = models.ForeignKey(
    #     UserCommitteeDocuments, null=True, blank=True, on_delete=models.PROTECT
    # )
    status = models.BooleanField(default=True, null=True, blank=True)


# अमानत कार्यादेश
class DepositMandate(BaseModel):
    """
    अमानत कार्यादेश
    """

    project = models.ForeignKey(
        ProjectExecution, on_delete=models.PROTECT, null=True, blank=True
    )
    mandate_type = models.CharField(
        max_length=30, null=True, blank=True, choices=MANDATE_TYPE
    )
    order_by = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="dm_order_by",
    )
    order_by_position = models.ForeignKey(
        EmployeeSector,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="dm_order_by_position",
    )
    order_date = models.CharField(max_length=50, null=True, blank=True)
    order_date_eng = models.DateField(null=True, blank=True)
    nominated_employee = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="dm_nominated_employees",
    )
    nominated_employee_position = models.ForeignKey(
        EmployeeSector,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="dm_nominated_employees_position",
    )
    invoice_date = models.CharField(max_length=50, null=True, blank=True)
    invoice_date_eng = models.DateField(null=True, blank=True)
    invoice_no = models.CharField(max_length=32, blank=True, null=True)
    latter_no = models.CharField(max_length=32, blank=True, null=True)
    work_complete_date = models.CharField(max_length=50, blank=True, null=True)
    work_complete_date_eng = models.DateField(max_length=32, blank=True, null=True)
    opinion = models.CharField(max_length=255, blank=True, null=True)
    report_custom_print = models.BooleanField(default=False)
    status = models.BooleanField(default=True, null=True, blank=True)


# संस्थागत सहकार्य
class InstitutionalCollaborationNominatedStaff(BaseModel):
    project = models.ForeignKey(
        ProjectExecution, on_delete=models.PROTECT, null=True, blank=True
    )
    code = models.CharField(max_length=10, null=True, blank=True)
    employee_name = models.ForeignKey(
        Employee, on_delete=models.PROTECT, null=True, blank=True
    )
    position = models.ForeignKey(
        EmployeeSector, null=True, blank=True, on_delete=models.PROTECT
    )
    remarks = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.IntegerField(null=True, blank=True)
    employee_name_by = models.CharField(max_length=150, blank=True, null=True)
    employee_position_by = models.CharField(max_length=150, blank=True, null=True)
    employee_name_remarks = models.CharField(max_length=150, blank=True, null=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class InstitutionalCollaborationMandate(BaseModel):
    project = models.ForeignKey(
        ProjectExecution, on_delete=models.PROTECT, null=True, blank=True
    )
    selected_employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, null=True, blank=True
    )
    opinion_detail = models.CharField(max_length=150, blank=True, null=True)
    invoice_number = models.DateField(null=True, blank=True)
    invoice_number_eng = models.DateField(null=True, blank=True)
    project_complete_date = models.DateField(null=True, blank=True)
    project_complete_date_eng = models.DateField(null=True, blank=True)
    mandate_invoice_no = models.CharField(max_length=20, blank=True, null=True)
    mandate_letter = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class ProjectReportFinishedAndUpdate(ProjectExecution):
    firm_name = models.ForeignKey(
        Organization, on_delete=models.PROTECT, null=True, blank=True
    )
    consumer_committee_name = models.ForeignKey(
        ConsumerCommittee, on_delete=models.PROTECT, null=True, blank=True
    )
    # भौतिक लक्ष्य
    quantity = models.CharField(max_length=100, null=True, blank=True)
    expense_investment = models.CharField(
        max_length=100, null=True, blank=True, help_text="लगत ईष्टिमेट "
    )
    unit_type = models.ForeignKey(
        Unit,
        related_name="prf_unit_type",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    # स्रोत व्यहोर्ने निकायहरू
    bid_calling_date = models.CharField(max_length=50, null=True, blank=True)
    bid_calling_date_eng = models.CharField(max_length=50, null=True, blank=True)
    bid_enter_date = models.CharField(max_length=50, null=True, blank=True)
    bid_enter_date_eng = models.CharField(max_length=50, null=True, blank=True)
    karyadesh_date = models.CharField(max_length=50, null=True, blank=True)
    karyadesh_date_eng = models.CharField(max_length=50, null=True, blank=True)
    bid_enter_number = models.IntegerField(
        null=True, blank=True, help_text="बोलपत्रको दाखिला संख्या:"
    )
    news_paper = models.ForeignKey(
        NewsPaper, on_delete=models.PROTECT, null=True, blank=True
    )
    published_date = models.CharField(max_length=50, null=True, blank=True)
    published_date_eng = models.CharField(max_length=50, null=True, blank=True)
    anticipated_completion_date = models.CharField(max_length=50, null=True, blank=True)
    anticipated_completion_date_eng = models.CharField(
        max_length=50, null=True, blank=True
    )
    agreement_date = models.CharField(max_length=50, null=True, blank=True)
    agreement_date_eng = models.CharField(max_length=50, null=True, blank=True)
    # भेरियसन
    expense_investment_variation = models.CharField(
        max_length=100, null=True, blank=True
    )
    variation_ru = models.CharField(max_length=50, null=True, blank=True)
    variation_percent = models.CharField(max_length=3, null=True, blank=True)
    variation_for_approval = models.CharField(
        max_length=100, null=True, blank=True, help_text="संसोधित लागत (रू.)"
    )
    ammended_expense = models.CharField(
        max_length=100, null=True, blank=True, help_text="संसोधित लागत (रू.)"
    )
    advanced = models.CharField(max_length=100, null=True, blank=True, help_text="पेश्की")
    paid = models.CharField(
        max_length=100, null=True, blank=True, help_text="भुक्तानी (पेश्की फछ्र्यौट)"
    )
    blocked_amount = models.CharField(max_length=100, null=True, blank=True)
    payment_remained = models.CharField(max_length=100, null=True, blank=True)
    finished_date = models.CharField(max_length=50, null=True, blank=True)
    finished_date_eng = models.CharField(max_length=50, null=True, blank=True)

    # योजनाको संक्ष्क्षिप्त भौतिक विवरण
    road_length = models.CharField(max_length=50, null=True, blank=True)
    road_width = models.CharField(max_length=50, null=True, blank=True)
    channel_length = models.CharField(max_length=50, null=True, blank=True)
    channel_depth = models.CharField(max_length=50, null=True, blank=True)
    drinking_water_pipe_length = models.CharField(max_length=50, null=True, blank=True)
    kalvert_length = models.CharField(max_length=50, null=True, blank=True)
    kalvert_width = models.CharField(max_length=50, null=True, blank=True)
    building_length = models.CharField(max_length=50, null=True, blank=True)
    building_width = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    total_storey = models.CharField(max_length=50, null=True, blank=True)
    wall_length = models.CharField(max_length=50, null=True, blank=True)
    wall_height = models.CharField(max_length=50, null=True, blank=True)
    source_preservation_area = models.CharField(max_length=50, null=True, blank=True)
    karmagat = models.IntegerField(null=True, blank=True)


class OfficialProcess(BaseModel):
    request_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="request_by_user"
    )
    send_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="action_taken_by",
    )
    parent_process = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="child_processes",
    )
    remarks = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="uploads/", null=True, blank=True)
    send_for = models.CharField(
        max_length=1, choices=RequestSend.choices, default=RequestSend.PREPARATION
    )
    feedback_remarks = models.TextField(null=True, blank=True)
    feedback_file = models.FileField(upload_to="uploads/", null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=ProcessStatus.choices, default=ProcessStatus.PENDING
    )
    project = models.ForeignKey(
        ProjectExecution, null=True, blank=True, on_delete=models.CASCADE
    )
    status_of_model = models.BooleanField(default=True, blank=True)


class OfficialProcessRemarkFile(BaseModel):
    file = models.FileField(upload_to="project_comment_remarks/")
    filename = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    official_process = models.ForeignKey(
        OfficialProcess,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="official_process_files",
    )


class ProjectCommentRemarkFile(BaseModel):
    file = models.FileField(upload_to="project_comment_remarks/")
    filename = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    individual_comment = models.ForeignKey(
        "plan_execution.IndividualProjectComment",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="individual_comment_files",
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        if not self.filename:
            self.filename = self.file.name
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        name = self.filename + " file of"
        if self.project_comment.exists():
            if self.project_comment.first().project:
                name += " " + self.project_comment.first().project.name + "'s comment"
            else:
                name += (
                    " "
                    + self.project_comment.first().get_send_for_display()
                    + " comment"
                )
        return name

    class Meta:
        verbose_name = "Project Comment Remark File"
        verbose_name_plural = "Project Comment Remark Files"


class CommentAndOrder(BaseModel):
    project = models.ForeignKey(
        ProjectExecution, null=True, blank=True, on_delete=models.CASCADE
    )
    cha_no = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Invoice Number",
        help_text="चलानी नं",
    )


class ProjectComment(BaseModel):
    """टिप्पणी model for the projects.

    Args:
        BaseModel (django.models.Model): Base Model to inherit the common fields.
    """

    project = models.ForeignKey(
        ProjectExecution, null=True, blank=True, on_delete=models.CASCADE
    )
    request_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="requested_comments",
        null=True,
        blank=True,
    )
    is_draft = models.BooleanField(default=False)
    is_signed = models.BooleanField(default=False)
    start_pms_process = models.ForeignKey(
        StartPmsProcess, null=True, blank=True, on_delete=models.PROTECT
    )
    process_name = models.CharField(
        max_length=255,
        choices=ProcessNameChoices.choices,
        default=ProcessNameChoices.MEASURING_BOOK,
    )
    status = models.CharField(
        max_length=1,
        choices=CommentStatusChoices.choices,
        default=CommentStatusChoices.PENDING,
    )
    send_for = models.CharField(
        max_length=1,
        choices=CommentSentForChoices.choices,
        default=CommentSentForChoices.PREPARATION,
    )
    remarks = models.TextField(null=True, blank=True)
    remark_files = models.ManyToManyField(
        ProjectCommentRemarkFile, blank=True, related_name="project_comment"
    )
    send_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="received_comment_requests",
    )
    last_status_update = models.DateTimeField(null=True, blank=True)
    last_status_updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="last_status_updated_comments",
    )
    users_allowed_to_comment = models.ManyToManyField(
        User, blank=True, related_name="commentable_project_comments"
    )

    def __str__(self) -> str:
        string = f"{self.get_send_for_display()} Comment"
        if self.project:
            string += f" for {self.project.name}"
        return string


class IndividualProjectComment(BaseModel):
    project_comment = models.ForeignKey(
        ProjectComment, on_delete=models.CASCADE, related_name="individual_comments"
    )
    commented_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="individual_comments",
    )
    comment = models.TextField(null=True, blank=True)
    comment_date_time = models.DateTimeField(auto_now_add=True)

    def add_comment_files(self, files: list):
        for file in files:
            self.individual_comment_files.create(file=file)


class ProjectModifiedReport(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="modified_reports",
    )
    start_pms_process = models.ForeignKey(
        StartPmsProcess,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="modified_reports",
    )
    report_type = models.ForeignKey(
        ReportType,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="modified_reports",
    )
    report_content = models.TextField(null=True, blank=True)
    report_file = models.FileField(upload_to="modified_reports/", null=True, blank=True)
    generated_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return (
            f"{self.project.name} - {self.report_type.name}"
            if self.project and self.report_type
            else str(self.id)
        )

    class Meta:
        verbose_name = "Project Modified Report"
        verbose_name_plural = "Project Modified Reports"


# Quotation Models
class FirmQuotedCostEstimate(BaseModel):
    firm = models.ForeignKey(
        "plan_execution.QuotationFirmDetails",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="quoted_cost_estimates",
    )
    cost_estimate_data = models.ForeignKey(
        "plan_execution.CostEstimateData",
        on_delete=models.CASCADE,
        related_name="firm_quoted_cost_estimate",
    )
    rate = models.CharField(max_length=255, null=True, blank=True)
    amount = models.CharField(max_length=255, null=True, blank=True)
    is_vat_added = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.firm.firm_name} - {self.cost_estimate_data.description}"

    @property
    def amount_in_number(self):
        value = self.amount
        try:
            value = int(value)
        except ValueError:
            value = value.replace(" ", "")
            locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
            value = locale.atof(value)
        except TypeError:
            value = 0
        return value

    class Meta:
        ordering = ["firm__id"]
        verbose_name = "Quotation: Firm Quoted Cost Estimate"
        verbose_name_plural = "Quotation: Firm Quoted Cost Estimates"


class QuotationFirmDetails(BaseModel):
    firm_name = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="quot_firm",
    )
    registration_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Registration Number",
        help_text="दर्ता नं",
    )
    pan_no = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="PAN Number",
        help_text="प्यान नं",
    )
    municipality = models.ForeignKey(
        "project.Municipality",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="quotation_firm_details",
    )
    ward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    tole = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    quot_specification = models.ForeignKey(
        "plan_execution.QuotationSpecification",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="specification_firm_details",
    )
    submission_approval = models.ForeignKey(
        "plan_execution.QuotationSubmissionApproval",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="submission_approval_firm_details",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Quotation: Firm Details"
        verbose_name_plural = "Quotation: Firm Details"

    def create_invitation(self):
        invitations = QuotationInvitationForProposal.objects.filter(
            invited_firm=self, project=self.quot_specification.project
        )
        if invitations.exists():
            return invitations.first()
        else:
            invitation = QuotationInvitationForProposal.objects.create(
                invited_firm=self,
                project=(
                    self.quot_specification.project if self.quot_specification else None
                ),
            )
        return invitation

    @property
    def cost_estimate_subtotal(self):
        return sum(
            [
                cost_estimate_data.amount_in_number
                for cost_estimate_data in self.quoted_cost_estimates.all()
            ]
        )

    @property
    def vat_amount(self):
        return self.cost_estimate_subtotal * 0.13

    @property
    def contingency_amount(self):
        return self.cost_estimate_subtotal * 0.015

    @property
    def total_amount(self):
        return self.cost_estimate_subtotal + self.vat_amount + self.contingency_amount

    def create_firm_quoted_cost_estimate(self):
        for cost_estimate_data in self.quot_specification.cost_estimate_data.all():
            FirmQuotedCostEstimate.objects.get_or_create(
                firm=self,
                cost_estimate_data=cost_estimate_data,
            )


class CostEstimateData(BaseModel):
    description = models.CharField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    rate = models.CharField(max_length=255, null=True, blank=True)
    amount = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    quot_specification = models.ForeignKey(
        "plan_execution.QuotationSpecification",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="cost_estimate_data",
    )

    @property
    def amount_in_number(self):
        value = self.amount
        try:
            value = int(value)
        except ValueError:
            value = value.replace(" ", "")
            locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
            value = locale.atof(value)
        except TypeError:
            value = 0
        return value

    class Meta:
        verbose_name = "Quotation: Cost Estimate Data"
        verbose_name_plural = "Quotation: Cost Estimate Data"


class QuotationSubmissionApproval(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="quot_submissions",
    )
    cha_no = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Invoice Number",
        help_text="चलानी नं",
    )
    letter_no = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Letter Number",
        help_text="पत्र नं",
    )
    date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Date",
        help_text="मिति",
    )
    date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Date (AD)",
        help_text="मिति (AD)",
    )

    class Meta:
        verbose_name = "Quotation: Submission Approval"
        verbose_name_plural = "Quotation: Submission Approvals"

    @property
    def quot_specification(self):
        return self.project.quot_specification.first()


class QuotationSpecification(BaseModel):
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="quot_specification",
    )
    cha_no = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Invoice Number",
        help_text="चलानी नं",
    )
    boq_type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="BOQ Type",
        help_text="बीओक्यू प्रकार",
        choices=BOQTypeChoices.choices,
    )
    letter_no = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Letter Number",
        help_text="पत्र नं",
    )
    date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Date",
        help_text="मिति",
    )
    date_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Date (AD)",
        help_text="मिति (AD)",
    )

    class Meta:
        verbose_name = "Quotation: Specification"
        verbose_name_plural = "Quotation: Specifications"

    @property
    def qsa(self):
        return self.project.quot_submissions.first()

    @property
    def cost_estimate_subtotal(self):
        return sum(
            [
                cost_estimate_data.amount_in_number
                for cost_estimate_data in self.cost_estimate_data.all()
            ]
        )

    @property
    def vat_amount(self):
        return self.cost_estimate_subtotal * 0.13

    @property
    def contingency_amount(self):
        return self.cost_estimate_subtotal * 0.015

    @property
    def total_amount(self):
        return self.cost_estimate_subtotal + self.vat_amount + self.contingency_amount

    def create_submission_approval(self):
        if self.project:
            if self.project.quot_submissions.exists():
                return self.project.quot_submissions.first()
            return QuotationSubmissionApproval.objects.create(
                project=self.project,
            )
        return None


class QuotationInvitationForProposal(BaseModel):
    invited_firm = models.ForeignKey(
        QuotationFirmDetails,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="quot_invited_for",
    )
    project = models.ForeignKey(
        ProjectExecution,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="quot_firm_invitations",
    )
    letter_no = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Letter Number",
        help_text="पत्र नं",
    )
    cha_no = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Invoice Number",
        help_text="चलानी नं",
    )

    class Meta:
        verbose_name = "Quotation: Invitation For Proposal"
        verbose_name_plural = "Quotation: Invitations For Proposal"

    @property
    def quot_specification(self) -> QuotationSpecification | None:
        return self.project.quot_specification.first()
