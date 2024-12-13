from django.db import models

from base_model.models import (
    Address,
    CommonFieldsBase,
    ContactDetail,
    ContactPerson,
    DocumentType,
)
from project.models import BaseModel, FinancialYear, Unit
from utils.nepali_nums import nepali_nums

# Create your models here.


class ExpanseType(CommonFieldsBase):
    is_addition = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectType(CommonFieldsBase):
    """
    self relating model
    योजनाको प्रकार
    """

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Parent Project Type",
        help_text="अभिभावक योजना प्रकार",
    )

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class PurposePlan(CommonFieldsBase):
    """
    योजनाको उदेश्य
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectProcess(CommonFieldsBase):
    """
    योजना संचालन प्रक्रिया
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectNature(CommonFieldsBase):
    """
    योजना प्रकृति
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectLevel(CommonFieldsBase):
    """
    योजनाको स्तर
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectProposedType(CommonFieldsBase):
    """
    योजनाको प्रस्ताबित प्रकार
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectActivity(CommonFieldsBase):
    """
    योजना क्रियाकलाप
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class PurchaseType(CommonFieldsBase):
    """
    खरिदको प्रकार
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class PriorityType(CommonFieldsBase):
    """
    प्राथिमिकताको  प्रकार
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class SelectionFeasibility(CommonFieldsBase):
    """
    योजना छनौटको आधार
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class StrategicSign(CommonFieldsBase):
    """
    रणनीतिक संकेत
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class Program(CommonFieldsBase):
    """self FK model
    कार्यकर्म
    """

    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class TargetGroupCategory(CommonFieldsBase):
    """
    लक्षित समुहको प्रकार
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class TargetGroup(CommonFieldsBase):
    """
    लक्षित समुह
    """

    target_group_category = models.ForeignKey(
        TargetGroupCategory, on_delete=models.PROTECT, null=True, blank=True
    )
    karmagat = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectStatus(CommonFieldsBase):
    """
    योजनाको अवस्था
    """

    karmagat = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ContractorType(CommonFieldsBase):
    """
    ठेकदरर्को प्रकार
    """

    karmagat = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class SubjectArea(CommonFieldsBase):
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Parent Subject Area",
        help_text="अभिभावक विषय क्षेत्र",
    )

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class OrganizationType(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class Office(CommonFieldsBase):
    organization_type = models.ForeignKey(
        OrganizationType, on_delete=models.PROTECT, null=True, blank=True
    )
    full_name = models.CharField(max_length=150, blank=True, null=True)
    full_name_eng = models.CharField(max_length=150, blank=True, null=True)
    registration_no = models.CharField(max_length=100, blank=True, null=True)
    registration_date = models.CharField(max_length=100, blank=True, null=True)
    registration_date_eng = models.CharField(max_length=100, blank=True, null=True)
    office = models.CharField(max_length=200, blank=True, null=True)
    detail = models.CharField(max_length=200, blank=True, null=True)
    current_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="office_crr_address",
        blank=True,
        null=True,
    )
    former_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="office_former_address",
        blank=True,
        null=True,
    )
    contact_person = models.ForeignKey(
        ContactPerson,
        on_delete=models.PROTECT,
        related_name="office_contact_person",
        blank=True,
        null=True,
    )
    contact_detail = models.ForeignKey(
        ContactDetail,
        on_delete=models.PROTECT,
        related_name="office_contact_detail",
        blank=True,
        null=True,
    )
    status = models.BooleanField(default=True, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    kramagat = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Currency(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class Module(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class SubModule(CommonFieldsBase):
    remarks = models.CharField(max_length=255, null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class NewsPaper(CommonFieldsBase):
    news_paper_address = models.CharField(max_length=255, null=True, blank=True)
    printing_house = models.CharField(max_length=255, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    contact_no = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ProjectStartDecision(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ConstructionMaterialDescription(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


# बजेट तथा स्रोत व्यवस्थापन -->
class BudgetSubTitle(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class PaymentMethod(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class SourceReceipt(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


#
class CollectPayment(CommonFieldsBase):
    """
    भुक्तानी माध्यम
    """

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class SubLedger(CommonFieldsBase):
    karmagat = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class AccountTitleManagement(CommonFieldsBase):
    CURRENT_CAPITAL = (("हालको", "हालको"), ("पुँजीगत", "पुँजीगत"), ("दुवै", "दुवै"))
    optional_code = models.CharField(max_length=55, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    display_name_eng = models.CharField(max_length=255, blank=True, null=True)
    is_budgeted = models.BooleanField(default=False)
    sapati = models.BooleanField(default=False)
    transfer_account = models.BooleanField(default=False)
    fund_account = models.BooleanField(default=False)
    base_account = models.BooleanField(default=False)
    is_transactable = models.BooleanField(default=False)
    current_capital = models.CharField(
        choices=CURRENT_CAPITAL, max_length=100, null=True, blank=True
    )
    current_ratio = models.CharField(max_length=255, blank=True, null=True)
    capital_ratio = models.CharField(max_length=255, blank=True, null=True)
    module = models.ForeignKey(
        SubModule,
        null=True,
        blank=True,
        related_name="atm_module",
        on_delete=models.PROTECT,
    )
    sub_module = models.ForeignKey(
        SubModule,
        null=True,
        blank=True,
        related_name="atm_submodule",
        on_delete=models.PROTECT,
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
    )
    financial_year = models.ForeignKey(
        FinancialYear, null=True, blank=True, on_delete=models.PROTECT
    )
    remarks = models.TextField(blank=True, default="")
    status = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return str(f"{self.code} - {self.name}")

    def has_children(self) -> bool:
        return self.children.exists()

    @property
    def estimated_expenditure_amount(self):
        expenditure_amount = 0
        if self.has_children():
            expenditure_amount += sum(
                [
                    child.estimated_expenditure_amount
                    for child in self.children.prefetch_related(
                        "budget_expenses",
                    )
                ]
            )
        if self.budget_expenses.exists():
            expenditure_amount += sum(
                [
                    float(budget_expense.estimated_expense_amount)
                    for budget_expense in self.budget_expenses.all()
                    if budget_expense.estimated_expense_amount
                ]
            )
        return expenditure_amount

    @property
    def revised_expenditure_amount(self):
        expenditure_amount = 0
        if self.has_children():
            expenditure_amount += sum(
                [
                    child.revised_expenditure_amount
                    for child in self.children.prefetch_related(
                        "budget_expenses",
                    )
                ]
            )
        if self.budget_expenses.exists():
            expenditure_amount += sum(
                [
                    float(budget_expense.revised_expense_amount)
                    for budget_expense in self.budget_expenses.all()
                    if budget_expense.revised_expense_amount
                ]
            )
        return expenditure_amount


class BudgetSource(CommonFieldsBase):
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Parent Budget Source",
        help_text="अभिभावक बजेट स्रोत",
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone Number",
        help_text="फोन नं.",
    )
    email = models.CharField(
        max_length=120, blank=True, null=True, verbose_name="Email", help_text="इमेल"
    )
    country = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Country", help_text="देश"
    )
    address = models.CharField(
        max_length=220,
        blank=True,
        null=True,
        verbose_name="Address",
        help_text="ठेगाना",
    )

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class SourceBearerEntityType(CommonFieldsBase):
    karmagat = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


# KHATA MANAGEMENT


class PaymentMedium(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class BankType(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ChequeFormat(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class BFI(CommonFieldsBase):
    bank_type = models.ForeignKey(
        BankType,
        related_name="bank_type",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Bank Type",
        help_text="बैंक प्रकार",
    )
    cheque_format = models.ForeignKey(
        ChequeFormat,
        related_name="cheque_format",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Cheque Format",
        help_text="चेक फारमेट",
    )
    full_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Full Name (Nepali)",
        help_text="पूरा नाम (नेपाली)",
    )
    full_name_eng = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Full Name (English)",
        help_text="पूरा नाम (अंग्रेजी)",
    )
    registration_no = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registration No.",
        help_text="दर्ता नं.",
    )
    registration_date = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registration Date (BS)",
        help_text="दर्ता मिति (बि.स.)",
    )
    registration_date_eng = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registration Date (AD)",
        help_text="दर्ता मिति (ई.स.)",
    )
    office = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Office",
        help_text="कार्यालय",
    )
    detail = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Other Detail",
        help_text="अन्य विवरण",
    )
    current_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="bank_crr_address",
        blank=True,
        null=True,
        verbose_name="Current Address",
        help_text="हालको ठेगाना",
    )
    former_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="bank_former_address",
        blank=True,
        null=True,
        verbose_name="Former Address",
        help_text="भूतपूर्व ठेगाना",
    )
    contact_person = models.ForeignKey(
        ContactPerson,
        on_delete=models.PROTECT,
        related_name="bank_contact_person",
        blank=True,
        null=True,
        verbose_name="Contact Person",
        help_text="सम्पर्क व्यक्ति",
    )
    contact_detail = models.ForeignKey(
        ContactDetail,
        on_delete=models.PROTECT,
        related_name="bank_contact_detail",
        blank=True,
        null=True,
    )
    remarks = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Remarks",
        help_text="कैफियत",
    )
    kramagat = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Kramagat",
        help_text="क्रमागत",
    )

    def __str__(self):
        return self.full_name

    @property
    def phone_number(self):
        return self.contact_detail.phone_number

    @property
    def fax(self):
        return self.contact_detail.fax_number

    @property
    def email(self):
        return self.contact_detail.email


class BankAccount(CommonFieldsBase):
    account_no = models.CharField(max_length=255, null=True, blank=True)
    currency = models.ForeignKey(
        Currency, on_delete=models.PROTECT, null=True, blank=True
    )
    branch_code = models.CharField(max_length=255, null=True, blank=True)
    branch_name = models.CharField(max_length=255, null=True, blank=True)
    branch_name_eng = models.CharField(max_length=255, null=True, blank=True)
    bank_name = models.ForeignKey(BFI, on_delete=models.PROTECT, null=True, blank=True)
    sub_module = models.ForeignKey(
        SubModule, on_delete=models.PROTECT, null=True, blank=True
    )
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class MemberType(CommonFieldsBase):
    def __str__(self):
        return f"{str(self.code)} member name: {self.name}"


class OrganizationDocument(CommonFieldsBase):
    document_type = models.ForeignKey(
        DocumentType,
        related_name="organization_documents",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    organization = models.ForeignKey(
        "Organization",
        related_name="documents",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )


class OrganizationMember(CommonFieldsBase):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    full_name_eng = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    position_start_date = models.CharField(max_length=50, null=True, blank=True)
    position_start_date_eng = models.CharField(max_length=50, null=True, blank=True)
    position_end_date = models.CharField(max_length=50, null=True, blank=True)
    position_end_date_eng = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    address = models.CharField(max_length=220, blank=True, null=True)
    member_type = models.ForeignKey(
        MemberType,
        related_name="organization_members",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    organization = models.ForeignKey(
        "Organization",
        related_name="members",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )


class Organization(CommonFieldsBase):
    IS_LOAN = (("भु. पु.", "भु. पु."), ("हालको", "हालको"))
    organization_type = models.ForeignKey(
        OrganizationType,
        related_name="organization_type",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    is_loan = models.CharField(max_length=10, choices=IS_LOAN, null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    full_name_eng = models.CharField(max_length=255, blank=True, null=True)
    register_no = models.CharField(max_length=255, blank=True, null=True)
    register_date_bs = models.CharField(max_length=100, blank=True, null=True)
    register_date_eng = models.CharField(max_length=100, blank=True, null=True)
    office = models.CharField(max_length=255, blank=True, null=True)
    other_details = models.CharField(max_length=255, blank=True, null=True)
    pan_number = models.IntegerField(blank=True, null=True)
    current_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="org_current_address",
        blank=True,
        null=True,
    )
    former_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="org_former_address",
    )
    contact_detail = models.ForeignKey(
        ContactDetail,
        related_name="org_contact_detail",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    contact_person = models.ForeignKey(
        ContactPerson,
        on_delete=models.PROTECT,
        related_name="org_contact_person",
        blank=True,
        null=True,
    )
    remarks = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.full_name or self.full_name_eng or self.id

    @property
    def name_or_nepali_name(self):
        return f"{self.name}-{self.name_eng}"

    @property
    def contact(self):
        return self.contact_detail.phone_number

    @property
    def fax(self):
        return self.contact_detail.fax_number

    @property
    def email(self):
        return self.contact_detail.email


class AbstractBaseCommittee(CommonFieldsBase):
    date = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Date (BS)",
        help_text="मिति (बि.स.)",
    )
    date_eng = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Date (AD)",
        help_text="मिति (ई.स.)",
    )
    ward = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        verbose_name="Ward No.",
        help_text="वडा नं.",
    )
    full_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Full Name (Nepali)",
        help_text="पूरा नाम (नेपाली)",
    )
    full_name_eng = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Full Name (English)",
        help_text="पूरा नाम (अंग्रेजी)",
    )
    bank_acc_no = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Bank Account No.",
        help_text="बैंक खाता नं.",
    )
    bank_branch = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Bank Branch",
        help_text="बैंक शाखा",
    )
    consumer_comittee_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Consumer Committee Type",
        help_text="उपभोक्ता समिति प्रकार",
    )
    present_quantity = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Present Quantity",
        help_text="वर्तमान मात्रा",
    )
    member_quantity = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Member Quantity",
        help_text="सदस्य मात्रा",
    )
    witness = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Witness",
        help_text="साक्षी",
    )
    registration_no = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registration No.",
        help_text="दर्ता नं.",
    )
    registration_date = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registration Date (BS)",
        help_text="दर्ता मिति (बि.स.)",
    )
    registration_date_eng = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registration Date (AD)",
        help_text="दर्ता मिति (ई.स.)",
    )
    office = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Office",
        help_text="कार्यालय",
    )
    remarks = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Remarks",
        help_text="कैफियत",
    )
    kramagat = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Kramagat",
        help_text="क्रमागत",
    )

    class Meta:
        abstract = True


class AbstractBaseCommitteeMember(CommonFieldsBase):
    ethnicity = models.CharField(max_length=100, blank=True, null=True)
    is_monitoring_team_member = models.BooleanField(default=False, blank=True)
    tax_payer_type = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    grand_father_name = models.CharField(max_length=100, blank=True, null=True)
    first_name_eng = models.CharField(max_length=100, blank=True, null=True)
    middle_name_eng = models.CharField(max_length=100, blank=True, null=True)
    last_name_eng = models.CharField(max_length=100, blank=True, null=True)
    father_name_eng = models.CharField(max_length=100, blank=True, null=True)
    grand_father_name_eng = models.CharField(max_length=100, blank=True, null=True)
    dob = models.CharField(max_length=100, blank=True, null=True)
    dob_eng = models.CharField(max_length=100, blank=True, null=True)
    citizenship_no = models.CharField(max_length=100, blank=True, null=True)
    citizenship_start_date = models.CharField(max_length=100, blank=True, null=True)
    citizenship_start_date_eng = models.CharField(max_length=100, blank=True, null=True)
    citizenship_from = models.CharField(max_length=100, blank=True, null=True)
    passport = models.CharField(max_length=100, blank=True, null=True)
    passport_start_date = models.CharField(max_length=100, blank=True, null=True)
    passport_start_date_eng = models.CharField(max_length=100, blank=True, null=True)
    passport_start_district = models.CharField(max_length=100, blank=True, null=True)
    voter_no = models.CharField(max_length=100, blank=True, null=True)
    voter_start_date = models.CharField(max_length=100, blank=True, null=True)
    voter_start_date_eng = models.CharField(max_length=100, blank=True, null=True)
    voter_start_district = models.CharField(max_length=100, blank=True, null=True)
    permanent_acc_no = models.CharField(max_length=100, blank=True, null=True)
    other_detail = models.CharField(max_length=100, blank=True, null=True)
    position_start_date = models.CharField(max_length=100, blank=True, null=True)
    position_start_date_eng = models.CharField(max_length=100, blank=True, null=True)
    position_end_date = models.CharField(max_length=100, blank=True, null=True)
    position_end_date_eng = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    karmagat = models.CharField(max_length=50, blank=True, null=True)

    @property
    def full_name(self):
        name = ""
        if self.first_name:
            name += self.first_name
        if self.middle_name:
            name += f" {self.middle_name}"
        if self.last_name:
            name += f" {self.last_name}"
        return name

    class Meta:
        abstract = True


class AbstractBaseCommitteeDocument(BaseModel):
    document_file = models.FileField(upload_to="consumer_committee_documents/")
    document_name = models.CharField(max_length=255, blank=True, null=True)
    document_size = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class ConsumerCommitteeDocument(AbstractBaseCommitteeDocument):
    document_type = models.ForeignKey(
        DocumentType,
        related_name="consumer_committee_documents",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    consumer_committee = models.ForeignKey(
        "ConsumerCommittee",
        related_name="documents",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )


class MonitoringCommitteeDocument(AbstractBaseCommitteeDocument):
    document_type = models.ForeignKey(
        DocumentType,
        related_name="monitoring_committee_documents",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    monitoring_committee = models.ForeignKey(
        "MonitoringCommittee",
        related_name="documents",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )


class ConsumerCommitteeMember(AbstractBaseCommitteeMember):
    tax_payer = models.ForeignKey(
        "employee.TaxPayer",
        related_name="consumer_committee_members",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    member_type = models.ForeignKey(
        MemberType,
        related_name="ccm_members",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    gender = models.ForeignKey(
        "base_model.Gender",
        null=True,
        blank=True,
        related_name="ccm",
        on_delete=models.PROTECT,
        verbose_name="Gender",
        help_text="लिङ्ग",
    )
    religion = models.ForeignKey(
        "employee.Religion",
        null=True,
        blank=True,
        related_name="ccm",
        on_delete=models.PROTECT,
        verbose_name="Religion",
        help_text="धर्म",
    )
    language = models.ForeignKey(
        "employee.Language",
        null=True,
        blank=True,
        related_name="ccm",
        on_delete=models.PROTECT,
        verbose_name="Gender",
        help_text="लिङ्ग",
    )
    country = models.ForeignKey(
        "employee.Country",
        null=True,
        blank=True,
        related_name="ccm",
        on_delete=models.PROTECT,
        verbose_name="Gender",
        help_text="लिङ्ग",
    )
    nationality = models.ForeignKey(
        "employee.Nationality",
        null=True,
        blank=True,
        related_name="ccm",
        on_delete=models.PROTECT,
        verbose_name="Gender",
        help_text="लिङ्ग",
    )
    permanent_current_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="ccm_permanent_current_address",
        blank=True,
        null=True,
    )
    permanent_former_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="ccm_permanent_former_address",
        blank=True,
        null=True,
    )
    temporary_current_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="ccm_temporary_current_address",
        blank=True,
        null=True,
    )
    temporary_former_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="ccm_temporary_former_address",
        blank=True,
        null=True,
    )
    contact_details = models.ForeignKey(
        ContactDetail,
        related_name="ccm_contact_detail",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    position = models.ForeignKey(
        "employee.Position",
        related_name="ccm_position",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    position_level = models.ForeignKey(
        "employee.PositionLevel",
        related_name="ccm_position_level",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    consumer_committee = models.ForeignKey(
        "ConsumerCommittee",
        related_name="members",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("member_type",)

    @property
    def name_and_address(self):
        return f"{self.full_name} {self.permanent_current_address}"


class MonitoringCommitteeMember(AbstractBaseCommitteeMember):
    tax_payer = models.ForeignKey(
        "employee.TaxPayer",
        related_name="monitoring_committee_members",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    member_type = models.ForeignKey(
        MemberType,
        related_name="mcm_members",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    gender = models.ForeignKey(
        "base_model.Gender",
        null=True,
        blank=True,
        related_name="mcm",
        on_delete=models.PROTECT,
        verbose_name="Gender",
        help_text="लिङ्ग",
    )
    religion = models.ForeignKey(
        "employee.Religion",
        null=True,
        blank=True,
        related_name="mcm",
        on_delete=models.PROTECT,
        verbose_name="Religion",
        help_text="धर्म",
    )
    language = models.ForeignKey(
        "employee.Language",
        null=True,
        blank=True,
        related_name="mcm",
        on_delete=models.PROTECT,
        verbose_name="Gender",
        help_text="लिङ्ग",
    )
    country = models.ForeignKey(
        "employee.Country",
        null=True,
        blank=True,
        related_name="mcm",
        on_delete=models.PROTECT,
        verbose_name="Gender",
        help_text="लिङ्ग",
    )
    nationality = models.ForeignKey(
        "employee.Nationality",
        null=True,
        blank=True,
        related_name="mcm",
        on_delete=models.PROTECT,
        verbose_name="Gender",
        help_text="लिङ्ग",
    )
    permanent_current_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="mcm_permanent_current_address",
        blank=True,
        null=True,
    )
    permanent_former_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="mcm_permanent_former_address",
        blank=True,
        null=True,
    )
    temporary_current_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="mcm_temporary_current_address",
        blank=True,
        null=True,
    )
    temporary_former_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="mcm_temporary_former_address",
        blank=True,
        null=True,
    )
    contact_details = models.ForeignKey(
        ContactDetail,
        related_name="mcm_contact_detail",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    position = models.ForeignKey(
        "employee.Position",
        related_name="mcm_position",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    position_level = models.ForeignKey(
        "employee.PositionLevel",
        related_name="mcm_position_level",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    monitoring_committee = models.ForeignKey(
        "MonitoringCommittee",
        related_name="members",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    user_committee_monitoring = models.ForeignKey(
        "plan_execution.UserCommitteeMonitoring",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="User Committee Monitoring",
        help_text="उपभोक्ता समिति अनुगमन",
        related_name="monitor_committee",
    )


class MonitoringCommittee(AbstractBaseCommittee):
    contact_person = models.ForeignKey(
        ContactPerson,
        on_delete=models.PROTECT,
        related_name="mc_contact_person",
        blank=True,
        null=True,
        verbose_name="Contact Person",
        help_text="सम्पर्क व्यक्ति",
    )
    current_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="mc_current_address",
        blank=True,
        null=True,
        verbose_name="Current Address",
        help_text="हालको ठेगाना",
    )
    former_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="mc_former_address",
        verbose_name="Former Address",
        help_text="भूतपूर्व ठेगाना",
    )
    contact_detail = models.ForeignKey(
        ContactDetail,
        related_name="mc_contact_detail",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Contact Detail",
        help_text="सम्पर्क विवरण",
    )
    bank = models.ForeignKey(
        BFI,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Bank/Financial Institution",
        help_text="बैंक/वित्तीय संस्था",
    )

    @property
    def chairman(self):
        return self.members.filter(member_type__name_eng__icontains="chairman").first()

    @property
    def vice_president(self):
        return self.members.filter(
            member_type__name_eng__icontains="vice president"
        ).first()

    @property
    def secretary(self):
        return self.members.filter(member_type__name_eng__icontains="secretary").first()

    @property
    def treasurer(self):
        return self.members.filter(member_type__name_eng__icontains="treasurer").first()

    @property
    def monitoring_committee_chairman(self):
        return self.members.filter(
            member_type__name_eng__icontains="monitoring committee chairman"
        ).first()

    @property
    def invited_member(self):
        return self.members.filter(member_type__name_eng__icontains="invited").first()

    @property
    def __str(self):
        return self.full_name

    @property
    def phone_number(self):
        return self.contact_detail.phone_number

    @property
    def fax(self):
        return self.contact_detail.fax_number

    @property
    def email(self):
        return self.contact_detail.email


class ConsumerCommittee(AbstractBaseCommittee):
    contact_person = models.ForeignKey(
        ContactPerson,
        on_delete=models.PROTECT,
        related_name="cc_contact_person",
        blank=True,
        null=True,
        verbose_name="Contact Person",
        help_text="सम्पर्क व्यक्ति",
    )
    current_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="cc_current_address",
        blank=True,
        null=True,
        verbose_name="Current Address",
        help_text="हालको ठेगाना",
    )
    former_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="cc_former_address",
        verbose_name="Former Address",
        help_text="भूतपूर्व ठेगाना",
    )
    contact_detail = models.ForeignKey(
        ContactDetail,
        related_name="cc_contact_detail",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Contact Detail",
        help_text="सम्पर्क विवरण",
    )
    bank = models.ForeignKey(
        BFI,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Bank/Financial Institution",
        help_text="बैंक/वित्तीय संस्था",
    )

    @property
    def chairman(self):
        return self.members.filter(member_type__name_eng__icontains="chairman").first()

    @property
    def vice_president(self):
        return self.members.filter(
            member_type__name_eng__icontains="vice president"
        ).first()

    @property
    def secretary(self):
        return self.members.filter(member_type__name_eng__icontains="secretary").first()

    @property
    def treasurer(self):
        return self.members.filter(member_type__name_eng__icontains="treasurer").first()

    @property
    def monitoring_committee_chairman(self):
        return self.members.filter(
            member_type__name_eng__icontains="monitoring committee chairman"
        ).first()

    @property
    def invited_member(self):
        return self.members.filter(member_type__name_eng__icontains="invited").first()

    @property
    def __str(self):
        return self.full_name

    @property
    def phone_number(self):
        return self.contact_detail.phone_number

    @property
    def fax(self):
        return self.contact_detail.fax_number

    @property
    def email(self):
        return self.contact_detail.email


class ExecutiveAgency(CommonFieldsBase):
    contact_person = models.ForeignKey(
        ContactPerson,
        on_delete=models.PROTECT,
        related_name="ea_contact_person",
        blank=True,
        null=True,
        verbose_name="Contact Person",
        help_text="सम्पर्क व्यक्ति",
    )
    current_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="ea_current_address",
        blank=True,
        null=True,
        verbose_name="Current Address",
        help_text="हालको ठेगाना",
    )
    date = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Date (BS)",
        help_text="मिति (बि.स.)",
    )
    date_eng = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Date (AD)",
        help_text="मिति (ई.स.)",
    )
    former_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="ea_former_address",
        verbose_name="Former Address",
        help_text="भूतपूर्व ठेगाना",
    )
    contact_detail = models.ForeignKey(
        ContactDetail,
        related_name="ea_contact_detail",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Contact Detail",
        help_text="सम्पर्क विवरण",
    )
    ward = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        verbose_name="Ward No.",
        help_text="वडा नं.",
    )
    full_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Full Name (Nepali)",
        help_text="पूरा नाम (नेपाली)",
    )
    full_name_eng = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Full Name (English)",
        help_text="पूरा नाम (अंग्रेजी)",
    )
    bank = models.ForeignKey(
        BFI,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Bank/Financial Institution",
        help_text="बैंक/वित्तीय संस्था",
    )
    bank_acc_no = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Bank Account No.",
        help_text="बैंक खाता नं.",
    )
    bank_branch = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Bank Branch",
        help_text="बैंक शाखा",
    )
    consumer_comittee_type = models.ForeignKey(
        MemberType,
        related_name="ea_consumer_committee_type",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Consumer Committee Type",
        help_text="उपभोक्ता समिति प्रकार",
    )
    present_quantity = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Present Quantity",
        help_text="वर्तमान मात्रा",
    )
    member_quantity = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Member Quantity",
        help_text="सदस्य मात्रा",
    )
    witness = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Witness",
        help_text="साक्षी",
    )
    registration_no = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registration No.",
        help_text="दर्ता नं.",
    )
    registration_date = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registration Date (BS)",
        help_text="दर्ता मिति (बि.स.)",
    )
    registration_date_eng = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Registration Date (AD)",
        help_text="दर्ता मिति (ई.स.)",
    )
    office = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Office",
        help_text="कार्यालय",
    )
    remarks = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Remarks",
        help_text="कैफियत",
    )
    kramagat = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Kramagat",
        help_text="क्रमागत",
    )

    def __str__(self):
        return f"{self.id}, code:{self.code}"


# सुचिकृत विवरण
# views and serializer in basic description serializer
class StandingListType(CommonFieldsBase):
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    registration_no = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.registration_no


class StandingList(CommonFieldsBase):
    date = models.CharField(max_length=100, null=True, blank=True)
    date_eng = models.CharField(max_length=100, null=True, blank=True)
    standing_list_type = models.ForeignKey(
        StandingListType, null=True, blank=True, on_delete=models.PROTECT
    )
    registration_number = models.CharField(max_length=100, null=True, blank=True)
    organization = models.ForeignKey(
        Organization, null=True, blank=True, on_delete=models.PROTECT
    )
    financial_year = models.ForeignKey(
        FinancialYear, null=True, blank=True, on_delete=models.PROTECT
    )
    detail = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    current = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


# Road related models.


class RoadStatus(CommonFieldsBase):
    karmagat = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class RoadType(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class DrainageType(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class Road(CommonFieldsBase):
    road_type = models.ForeignKey(
        RoadType,
        related_name="road_type",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    road_status = models.ForeignKey(
        RoadStatus,
        related_name="road_status",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    average_width = models.IntegerField(null=True, blank=True)
    road_width_unit = models.ForeignKey(
        Unit,
        related_name="road_width_unit",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    road_length = models.IntegerField(null=True, blank=True)
    road_length_unit = models.ForeignKey(
        Unit,
        related_name="road_length_unit",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    connected_wards = models.CharField(max_length=100, null=True, blank=True)
    connected_roads = models.CharField(max_length=100, null=True, blank=True)
    total_consumer = models.CharField(max_length=100, null=True, blank=True)
    total_house = models.CharField(max_length=100, null=True, blank=True)
    road_start_from = models.CharField(max_length=100, null=True, blank=True)
    road_end_to = models.CharField(max_length=100, null=True, blank=True)
    other_status = models.CharField(max_length=100, null=True, blank=True)
    karmagat = models.IntegerField(null=True, blank=True)
    # Drainage
    drainage_exit_status = models.BooleanField(default=True)
    drainage_type = models.ForeignKey(
        DrainageType,
        related_name="drainage_type",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    drainage_width = models.IntegerField(null=True, blank=True)
    drainage_width_unit = models.ForeignKey(
        Unit,
        related_name="drainage_width_unit",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    drainage_length = models.IntegerField(null=True, blank=True)
    drainage_length_unit = models.ForeignKey(
        Unit,
        related_name="drainage_length_unit",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    remarks = models.CharField(max_length=255, null=True, blank=True)
    other_remarks = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class SourceBearerEntity(CommonFieldsBase):
    bearer_type = models.ForeignKey(
        SourceBearerEntityType,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="source_bearer_type",
    )
    organization_name = models.ForeignKey(
        Organization, null=True, blank=True, on_delete=models.PROTECT
    )
    karmagat = models.CharField(null=True, blank=True, max_length=5)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)
