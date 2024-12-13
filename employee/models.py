from django.db import models

from base_model.models import Address, CommonFieldsBase, ContactDetail, Gender
from project.models import BaseModel, District
from project_planning.models import BFI, PaymentMedium, SubjectArea
from utils.constants import POSITION_CHOICES, TAX_PAYER_TYPE

# Create your models here.


class MaritalStatus(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class Department(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class DepartmentBranch(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class PositionLevel(CommonFieldsBase):
    basic_salary = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Basic Salary",
        help_text="आधारभूत तलब",
    )
    maximum_grade_rate = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Maximum Grade Rate",
        help_text="अधिकतम ग्रेड रकम",
    )
    adjustment_grade_rate = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Adjustment Grade Rate",
        help_text="समायोजन ग्रेड दर",
    )
    position_type = models.CharField(
        max_length=10,
        choices=POSITION_CHOICES,
        null=True,
        blank=True,
        verbose_name="Position Type",
        help_text="पदको प्रकार",
    )
    short_form = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Short Form",
        help_text="छोटो फारम",
    )

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class Position(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class EmployeeType(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class ServiceGroup(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class EmployeeSector(CommonFieldsBase):
    insurance_amount = models.FloatField(null=True, blank=True, help_text="बिमा रकम")
    allowance_amount = models.FloatField(null=True, blank=True, help_text="भत्ता रकम")
    position_level = models.ForeignKey(
        PositionLevel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="श्रेणी/तह",
    )
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, null=True, blank=True
    )
    remarks = models.TextField(
        max_length=1_000, null=True, blank=True, help_text="कैफियत"
    )
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class CurrentWorkingDetail(BaseModel):
    department = models.ForeignKey(
        Department,
        related_name="current_department",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Department",
        help_text="विभाग",
    )
    department_branch = models.ForeignKey(
        DepartmentBranch,
        related_name="current_department_branch",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Department Branch",
        help_text="विभाग शाखा",
    )
    position_level = models.ForeignKey(
        PositionLevel,
        related_name="current_department_branch",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    work_area = models.ForeignKey(
        Position,
        related_name="current_department_branch",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    employee_type = models.ForeignKey(
        EmployeeType,
        related_name="current_department_branch",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    service_group = models.ForeignKey(
        ServiceGroup,
        related_name="current_service_group",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    position = models.ForeignKey(
        EmployeeSector,
        related_name="current_work_area",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    retirement_date = models.CharField(max_length=255, null=True, blank=True)
    retirement_date_eng = models.CharField(max_length=255, null=True, blank=True)
    leave_date = models.CharField(max_length=255, null=True, blank=True)
    leave_date_eng = models.CharField(max_length=255, null=True, blank=True)
    insurance_facility = models.BooleanField(default=False)
    penalty_deduction = models.BooleanField(default=False)
    payment_medium = models.ForeignKey(
        PaymentMedium, on_delete=models.PROTECT, null=True, blank=True
    )
    bank_name = models.ForeignKey(BFI, on_delete=models.PROTECT, null=True, blank=True)
    bank_sheet_no = models.CharField(max_length=200, blank=True, null=True)
    account_no = models.CharField(max_length=200, blank=True, null=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    kramagat = models.CharField(max_length=255, blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class FamilyDetail(BaseModel):
    father_name = models.CharField(
        max_length=255, blank=True, verbose_name="Father Name", help_text="बाबुको नाम"
    )
    father_name_eng = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Father Name (Eng)",
        help_text="बाबुको नाम (अंग्रेजी)",
    )
    mother_name = models.CharField(
        max_length=255, blank=True, verbose_name="Mother Name", help_text="आमाको नाम"
    )
    mother_name_eng = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Mother Name (Eng)",
        help_text="आमाको नाम (अंग्रेजी)",
    )
    spouse_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Spouse Name",
        help_text="श्रीमानको नाम",
    )
    spouse_name_eng = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Spouse Name (Eng)",
        help_text="श्रीमानको नाम (अंग्रेजी)",
    )
    wished_person_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Wished Person Name",
        help_text="इच्छुक व्यक्तिको नाम",
    )
    wished_person_name_eng = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Wished Person Name (Eng)",
        help_text="इच्छुक व्यक्तिको नाम (अंग्रेजी)",
    )


class EnrollmentDetail(BaseModel):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Department",
        help_text="विभाग",
    )
    position = models.ForeignKey(
        Position,
        related_name="enrollment_position",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Position",
        help_text="पद",
    )
    start_date = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Start Date",
        help_text="सुरु मिति",
    )
    end_date = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="End Date",
        help_text="अन्तिम मिति",
    )


class CumulativeDetail(BaseModel):
    book_store_no = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Book Store No",
        help_text="पुस्तक भण्डार नं",
    )
    employee_saving_funds_no = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Employee Saving Funds No",
        help_text="कर्मचारी बचत कोष नं",
    )
    permanent_article_no = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Permanent Article No",
        help_text="स्थायी लेखा नं",
    )
    citizen_investment_no = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Citizen Investment No",
        help_text="नागरिक लगानी नं",
    )
    cif_certificate_no = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="CIF Certificate No",
        help_text="सिफ सर्टिफिकेट नं",
    )
    citizen_investment_deduction_percent = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Citizen Investment Deduction Percent",
        help_text="नागरिक लगानी कटौती प्रतिशत",
    )
    insurance_company = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Insurance Company",
        help_text="बिमा कम्पनी",
    )
    insurance_policy_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Insurance Policy No",
        help_text="बिमा नीति नं",
    )
    insurance_amount = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Insurance Amount",
        help_text="बिमा रकम",
    )


class Employee(BaseModel):
    code = models.CharField(
        max_length=32, null=True, blank=True, verbose_name="Code", help_text="कोड"
    )
    first_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="First Name",
        help_text="पहिलो नाम",
    )
    first_name_eng = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="First Name (Eng)",
        help_text="पहिलो नाम (अंग्रेजी)",
    )
    middle_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Middle Name",
        help_text="बीचको नाम",
    )
    middle_name_eng = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Middle Name (Eng)",
        help_text="बीचको नाम (अंग्रेजी)",
    )
    last_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Last Name",
        help_text="थर",
    )
    last_name_eng = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Last Name (Eng)",
        help_text="थर (अंग्रेजी)",
    )
    dob = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Date of Birth",
        help_text="जन्म मिति",
    )
    dob_eng = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Date of Birth (Eng)",
        help_text="जन्म मिति (अंग्रेजी)",
    )
    gender = models.ForeignKey(
        Gender,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Gender",
        help_text="लिङ्ग",
    )
    contact_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Contact Number",
        help_text="सम्पर्क नं",
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Phone Number",
        help_text="फोन नं",
    )
    email = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Email", help_text="ईमेल"
    )
    image = models.ImageField(
        upload_to="uploads/employee/",
        null=True,
        blank=True,
        verbose_name="Image",
        help_text="तस्बिर",
    )
    marital_status = models.ForeignKey(
        MaritalStatus,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Marital Status",
        help_text="वैवाहिक स्थिति",
    )
    subject_area = models.ForeignKey(
        SubjectArea,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Subject Area",
        help_text="विषयगत कार्यक्षेत्र",
    )
    permanent_address = models.ForeignKey(
        Address,
        related_name="emp_permanent_address",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Permanent Address",
        help_text="स्थायी ठेगाना",
    )
    temporary_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="emp_temporary_address",
        null=True,
        blank=True,
        verbose_name="Temporary Address",
        help_text="अस्थायी ठेगाना",
    )
    current_working_details = models.ForeignKey(
        CurrentWorkingDetail,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Current Working Details",
        help_text="वर्तमान कार्यालय विवरण",
    )
    family_detail = models.ForeignKey(
        FamilyDetail,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Family Detail",
        help_text="परिवारको विवरण",
    )
    enrollment_detail = models.ForeignKey(
        EnrollmentDetail,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Enrollment Detail",
        help_text="नामानामाको विवरण",
    )
    cumulative_detail = models.ForeignKey(
        CumulativeDetail,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Cumulative Detail",
        help_text="जम्मा विवरण",
    )

    @property
    def full_name(self):
        return " ".join([self.first_name, self.middle_name, self.last_name])

    @property
    def full_name_eng(self):
        return " ".join([self.first_name_eng, self.middle_name_eng, self.last_name_eng])

    @property
    def department(self):
        return self.current_working_details.department.name

    @property
    def service(self):
        return "%s" % (self.current_working_details.service_group.name)

    @property
    def enroll_start_date(self):
        return "%s" % (self.enrollment_detail.start_date)

    def __str__(self):
        return str(self.full_name or self.id)


class TaxPayer(BaseModel):
    tax_payer_no = models.CharField(max_length=100, null=True, blank=True)
    internal_source_no = models.CharField(max_length=100, null=True, blank=True)
    tax_payer_name = models.CharField(max_length=100, null=True, blank=True)
    citizenship_no = models.CharField(max_length=100, null=True, blank=True)
    citizenship_from = models.ForeignKey(
        District, on_delete=models.PROTECT, null=True, blank=True
    )
    citizenship_register_date = models.CharField(max_length=100, null=True, blank=True)
    registration_no = models.CharField(max_length=100, null=True, blank=True)
    permanent_address = models.CharField(max_length=100, null=True, blank=True)
    gender = models.ForeignKey(Gender, null=True, blank=True, on_delete=models.PROTECT)
    dob = models.CharField(max_length=100, null=True, blank=True)
    contact_no = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    text_payer_type = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class Religion(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.code or self.id)


class Language(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.code or self.id)


class Country(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.code or self.id)


class Nationality(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.code or self.id)


class PublicRepresentativePosition(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.code or self.id)


class PublicRepresentativeDetail(BaseModel):
    representative_position = models.ForeignKey(
        PublicRepresentativePosition, null=True, blank=True, on_delete=models.PROTECT
    )
    tax_payer = models.ForeignKey(
        TaxPayer, null=True, blank=True, on_delete=models.PROTECT
    )
    tax_payer_type = models.CharField(
        max_length=30, null=True, blank=True, choices=TAX_PAYER_TYPE
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    grand_father_name = models.CharField(max_length=100, null=True, blank=True)
    first_name_eng = models.CharField(max_length=100, null=True, blank=True)
    middle_name_eng = models.CharField(max_length=100, null=True, blank=True)
    last_name_eng = models.CharField(max_length=100, null=True, blank=True)
    father_name_eng = models.CharField(max_length=100, null=True, blank=True)
    grand_father_name_eng = models.CharField(max_length=100, null=True, blank=True)
    dob = models.CharField(max_length=100, null=True, blank=True)
    dob_eng = models.CharField(max_length=100, null=True, blank=True)
    religion = models.ForeignKey(
        Religion, on_delete=models.PROTECT, null=True, blank=True
    )
    language = models.ForeignKey(
        Language, on_delete=models.PROTECT, null=True, blank=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, null=True, blank=True
    )
    nationality = models.ForeignKey(
        Nationality, on_delete=models.PROTECT, null=True, blank=True
    )
    citizenship_no = models.CharField(max_length=100, null=True, blank=True)
    citizenship_start_date = models.CharField(max_length=100, null=True, blank=True)
    citizenship_start_date_eng = models.CharField(max_length=100, null=True, blank=True)
    citizenship_from = models.CharField(max_length=100, null=True, blank=True)
    passport = models.CharField(max_length=100, null=True, blank=True)
    passport_start_date = models.CharField(max_length=100, null=True, blank=True)
    passport_start_date_eng = models.CharField(max_length=100, null=True, blank=True)
    passport_start_district = models.CharField(max_length=100, null=True, blank=True)
    voter_no = models.CharField(max_length=100, null=True, blank=True)
    voter_start_date = models.CharField(max_length=100, null=True, blank=True)
    voter_start_date_eng = models.CharField(max_length=100, null=True, blank=True)
    permanent_acc_no = models.CharField(max_length=100, null=True, blank=True)
    other_detail = models.CharField(max_length=100, null=True, blank=True)
    permanent_current_address = models.ForeignKey(
        Address,
        related_name="pc_address",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    permanent_former_address = models.ForeignKey(
        Address,
        related_name="pf_address",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    temporary_current_address = models.ForeignKey(
        Address,
        related_name="tc_address",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    temporary_former_address = models.ForeignKey(
        Address,
        related_name="tf_address",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    contact_details = models.ForeignKey(
        ContactDetail, null=True, blank=True, on_delete=models.PROTECT
    )
    position = models.ForeignKey(
        Position, null=True, blank=True, on_delete=models.PROTECT
    )
    position_level = models.ForeignKey(
        PositionLevel, null=True, blank=True, on_delete=models.PROTECT
    )
    position_start_date = models.CharField(max_length=50, null=True, blank=True)
    position_start_date_eng = models.CharField(max_length=50, null=True, blank=True)
    position_end_date = models.CharField(max_length=50, null=True, blank=True)
    position_end_date_eng = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.CharField(max_length=50, null=True, blank=True)
    karmagat = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    @property
    def email(self):
        return self.contact_details.email

    @property
    def mobile(self):
        return self.contact_details.mobile_number
