import nepali_datetime
from django.db import models

from utils.nepali_nums import nepali_nums


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        "user.User",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Created By",
        related_name="%(app_label)s_%(class)s_created_by",
        help_text="निर्माण गर्ने",
    )
    updated_by = models.ForeignKey(
        "user.User",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_updated_by",
        verbose_name="Updated By",
    )
    code = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Code",
        help_text="कोड",
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date", help_text="निर्माण मिति"
    )
    updated_date = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date", help_text="अद्यावधिक मिति"
    )
    status = models.BooleanField(default=True, verbose_name="Status", help_text="स्थिति")

    def __str__(self) -> str:
        return str(self.id)

    @property
    def is_used_in_relation(self):
        return any(
            [
                relation.related_model.objects.filter(
                    **{relation.field.name: self}
                ).exists()
                for relation in self._meta.related_objects
            ]
        )

    class Meta:
        abstract = True


class FederalType(BaseModel):
    name = models.CharField(
        blank=True, max_length=120, verbose_name="Name", help_text="नाम"
    )
    name_unicode = models.CharField(
        blank=True,
        max_length=120,
        verbose_name="Name (Unicode)",
        help_text="नाम (युनिकोड)",
    )
    name_eng = models.CharField(
        blank=True,
        max_length=120,
        verbose_name="Name (Eng)",
        help_text="नाम (अंग्रेजी)",
    )
    upper_federal_type = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Upper Federal Type",
        help_text="माथीको संघीय प्रकार",
    )

    class Meta:
        verbose_name = "Master Data: Federal Type"
        verbose_name_plural = "Master Data: Federal Types"

    def __str__(self):
        return self.name or self.name_eng or self.name_unicode


class FederalAbstractModel(BaseModel):
    name = models.CharField(
        blank=True, max_length=120, verbose_name="Name", help_text="नाम"
    )
    name_unicode = models.CharField(
        blank=True,
        max_length=120,
        verbose_name="Name (Unicode)",
        help_text="नाम (युनिकोड)",
    )
    name_eng = models.CharField(
        blank=True,
        max_length=120,
        verbose_name="Name (Eng)",
        help_text="नाम (अंग्रेजी)",
    )
    remarks = models.TextField(blank=True, verbose_name="Remarks", help_text="कैफियत")
    federal_type = models.ForeignKey(
        FederalType,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Federal Type",
        help_text="संघीय प्रकार",
    )

    class Meta:
        abstract = True


class Province(FederalAbstractModel):
    province_number = models.PositiveIntegerField(
        verbose_name="Province Number", help_text="प्रदेश नम्बर"
    )

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return self.name or self.name_eng or self.name_unicode


class District(FederalAbstractModel):
    province = models.ForeignKey(
        Province,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Province",
        help_text="प्रदेश",
    )

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return self.name or self.name_eng or self.name_unicode


class Municipality(FederalAbstractModel):
    class Meta:
        verbose_name_plural = "Municipalities"

    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="District",
        help_text="जिल्ला",
    )
    number_of_wards = models.PositiveSmallIntegerField(
        default=1, verbose_name="Number of Wards", help_text="वडा संख्या"
    )
    office_name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Office Name",
        help_text="कार्यालयको नाम",
    )
    sub_name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Sub Name",
        help_text="उपनाम",
    )
    office_address = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Office Address",
        help_text="कार्यालयको ठेगाना",
    )
    email = models.EmailField(
        max_length=100, null=True, blank=True, verbose_name="Email", help_text="ईमेल"
    )
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        default="",
        verbose_name="Phone",
        help_text="फोन",
    )

    @property
    def access_url(self):
        return f"{self.client.subdomain}" if self.client else None

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return self.name or self.name_unicode or self.name_eng


class Ward(BaseModel):
    municipality = models.ForeignKey(
        Municipality, on_delete=models.PROTECT, null=True, blank=True
    )
    ward_number = models.CharField(max_length=10)
    name = models.CharField(blank=True, max_length=120)
    name_unicode = models.CharField(blank=True, max_length=120)
    name_eng = models.CharField(blank=True, max_length=120)
    remarks = models.TextField(blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return f"{self.municipality}-{self.ward_number}"


class Topic(BaseModel):
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    name = models.TextField(blank=True)
    name_eng = models.TextField(blank=True)
    name_unicode = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        unique_together = ["parent", "name_eng", "name_unicode"]

    def __str__(self):
        return self._name

    # def check_before_save(self):
    #     if self.parent:
    #         if self.topic_set.filter(id=self.parent.id).exists():
    #             return False, "A child topic cannot be added as parent topic."
    #         if self.parent == self:
    #             return False, "A topic cannot be added into itself."
    #     return True, "All Good"

    # def save(
    #     self,
    #     force_insert: bool = ...,
    #     force_update: bool = ...,
    #     using: str | None = ...,
    #     update_fields: Iterable[str] | None = ...,
    # ) -> None:
    #     check, message = self.check_before_save()
    #     if not check:
    #         raise Exception(f"Error: {message}")
    #     return super().save(force_insert, force_update, using, update_fields)

    @property
    def _name(self):
        return self.name_unicode or self._name_eng

    @property
    def _name_eng(self):
        if self.parent:
            return f"{self.parent._name_eng}-----{self.name_eng}"
        return self.name_eng

    @property
    def _name_unicode(self):
        if self.parent:
            return f"{self.parent._name_unicode}-----{self.name_unicode}"
        return self.name_unicode

    @property
    def level(self):
        if self.parent:
            return self.parent.level + 1
        return 1


class FinancialYear(BaseModel):
    start_year = models.IntegerField(
        verbose_name="Start Year", help_text="आरम्भ वर्ष (बि.सं.)"
    )
    end_year = models.IntegerField(
        verbose_name="End Year", help_text="समाप्त वर्ष (बि.सं.)"
    )
    fy = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Financial Year",
        help_text="आर्थिक बर्ष",
    )

    @property
    def name(self):
        return f"{self.start_year}/{str(self.end_year)[2:]}"

    @property
    def nepali(self):
        return nepali_nums(self.fy or self.name)

    def __str__(self):
        return self.fy or self.name

    def save(self, *args, **kwargs):
        self.fy = f"{self.start_year}/{self.end_year}"
        super().save(*args, **kwargs)

    @classmethod
    def current_fy(cls):
        today = nepali_datetime.date.today()
        start = today.year
        if today.month < 4:
            start -= 1
        fy, _ = cls.objects.get_or_create(start_year=start, end_year=start + 1)
        return fy

    @classmethod
    def last_3_fys(cls):
        current_fy = cls.current_fy()
        prev_fy, _ = cls.objects.get_or_create(
            start_year=current_fy.start_year - 1, end_year=current_fy.start_year
        )
        prev_prev_fy, _ = cls.objects.get_or_create(
            start_year=prev_fy.start_year - 1, end_year=prev_fy.start_year
        )
        return [prev_prev_fy, prev_fy, current_fy]


class DistrictRateFiles(BaseModel):
    title = models.CharField(blank=True, max_length=255)
    district = models.ForeignKey(District, null=True, on_delete=models.PROTECT)
    municipality = models.ForeignKey(
        Municipality, on_delete=models.PROTECT, null=True, blank=True
    )
    financial_year = models.ForeignKey(
        FinancialYear, null=True, on_delete=models.PROTECT
    )
    file = models.FileField(upload_to="uploads/district_rates/")
    status = models.BooleanField(default=True, null=True, blank=True)


class ProjectCategory(BaseModel):
    name = models.CharField(
        blank=True, max_length=120, verbose_name="Name", help_text="नाम"
    )
    name_unicode = models.CharField(
        blank=True,
        max_length=120,
        verbose_name="Name (Unicode)",
        help_text="नाम (युनिकोड)",
    )
    name_eng = models.CharField(
        blank=True,
        max_length=120,
        verbose_name="Name (Eng)",
        help_text="नाम (अंग्रेजी)",
    )


class Project(BaseModel):
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Municipality",
        help_text="नगरपालिका",
    )
    ward = models.ManyToManyField(
        Ward, blank=True, verbose_name="Ward", help_text="वडा"
    )
    name = models.CharField(
        max_length=500, null=True, blank=True, verbose_name="Name", help_text="नाम"
    )

    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="projects",
        verbose_name="Category",
        help_text="श्रेणी",
    )

    financial_year = models.ForeignKey(
        FinancialYear,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Financial Year",
        help_text="आर्थिक बर्ष",
    )

    def __str__(self):
        return str(self.name or self.id)


class JobDescriptionStatusChoices(models.TextChoices):
    CREATED = "CREATED", "Created"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    INACTIVE = "INACTIVE", "Inactive"


class JobDescription(BaseModel):
    title = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="job_descriptions",
    )
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=JobDescriptionStatusChoices.choices,
        default=JobDescriptionStatusChoices.CREATED,
    )

    approved_by = models.ForeignKey(
        "user.user",
        on_delete=models.PROTECT,
        related_name="approved_job_descriptions",
        null=True,
        blank=True,
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    status_of_model = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.title


class JDComment(BaseModel):
    text = models.TextField()
    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.PROTECT,
        related_name="comments",
        null=True,
        blank=True,
    )
    status = models.BooleanField(default=True, null=True, blank=True)


class JobDescriptionFile(BaseModel):
    file_type = models.CharField(max_length=255)
    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.PROTECT,
        null=True,
        related_name="files",
        blank=True,
    )

    file = models.FileField(upload_to="upload/jd/")
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return f"{self.job_description} {self.file_type}"


class RateCategory(BaseModel):
    municipality = models.ForeignKey(
        Municipality, null=True, on_delete=models.PROTECT, blank=True
    )
    name = models.CharField(blank=True, max_length=120)
    name_unicode = models.CharField(blank=True, max_length=120)
    name_eng = models.CharField(blank=True, max_length=120)
    remarks = models.TextField(blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class Unit(BaseModel):
    municipality = models.ForeignKey(
        Municipality,
        null=True,
        on_delete=models.PROTECT,
        blank=True,
        verbose_name="Municipality",
        help_text="नगरपालिका",
    )
    code = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Code", help_text="कोड"
    )
    name = models.CharField(
        blank=True, max_length=120, verbose_name="Name", help_text="नाम"
    )
    name_unicode = models.CharField(
        blank=True,
        max_length=120,
        verbose_name="Name (Unicode)",
        help_text="नाम (युनिकोड)",
    )
    name_eng = models.CharField(
        blank=True,
        max_length=120,
        verbose_name="Name (Eng)",
        help_text="नाम (अंग्रेजी)",
    )
    remarks = models.TextField(blank=True, verbose_name="Remarks", help_text="कैफियत")

    def __str__(self):
        return self.name_unicode or self.name_eng or self.name


class RateArea(BaseModel):
    municipality = models.ForeignKey(
        Municipality, null=True, on_delete=models.PROTECT, blank=True
    )
    name = models.CharField(blank=True, max_length=120)
    name_unicode = models.CharField(blank=True, max_length=120)
    name_eng = models.CharField(blank=True, max_length=120)
    remarks = models.TextField(blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.name_unicode or self.name_eng or self.name


class RateSource(BaseModel):
    municipality = models.ForeignKey(
        Municipality, null=True, on_delete=models.PROTECT, blank=True
    )
    name = models.CharField(blank=True, max_length=120)
    name_unicode = models.CharField(blank=True, max_length=120)
    name_eng = models.CharField(blank=True, max_length=120)
    remarks = models.TextField(blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.name_unicode or self.name_eng or self.name


class Rate(BaseModel):
    """
    Each municipality will have its own version of district rate instead of having district level data
    """

    district = models.ForeignKey(
        District, null=True, on_delete=models.PROTECT, blank=True
    )
    municipality = models.ForeignKey(
        Municipality, on_delete=models.PROTECT, null=True, blank=True
    )
    financial_year = models.ForeignKey(
        FinancialYear, null=True, on_delete=models.PROTECT, blank=True
    )
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, null=True, blank=True)
    category = models.ForeignKey(
        RateCategory, on_delete=models.PROTECT, null=True, blank=True
    )

    title = models.TextField(blank=True, default="")
    title_eng = models.TextField(blank=True, default="")

    # Amount in the lowest denomination (paisa)
    amount = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, default="0.0"
    )
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True)
    source = models.ForeignKey(RateSource, on_delete=models.PROTECT, null=True)
    area = models.ForeignKey(RateArea, on_delete=models.PROTECT, null=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def level(self):
        return self.topic.level


class Estimate(BaseModel):
    project = models.OneToOneField(Project, on_delete=models.PROTECT, null=True)
    file = models.FileField(upload_to="uploads/estimate/", blank=True, null=True)
    title = models.CharField(max_length=255)
    road_1_rate = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, default="0.0"
    )
    road_2_rate = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, default="0.0"
    )
    road_3_rate = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, default="0.0"
    )

    summary_of_project = models.BooleanField(default=True)
    abstract_of_cost = models.BooleanField(default=True)
    summary_of_rates = models.BooleanField(default=True)
    district_rate = models.BooleanField(default=True)
    transportation_of_material = models.BooleanField(default=True)
    rate_analysis_of_general_work = models.BooleanField(default=True)
    detailed_quantity_calculation = models.BooleanField(default=True)
    material_cost_with_transport = models.BooleanField(default=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class EstimationRate(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True)
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)

    length = models.DecimalField(default=0, max_digits=20, decimal_places=5)
    breadth = models.DecimalField(default=0, max_digits=20, decimal_places=5)
    height = models.DecimalField(default=0, max_digits=20, decimal_places=5)
    area = models.DecimalField(default=0, max_digits=20, decimal_places=5)
    quantity = models.DecimalField(default=0, max_digits=20, decimal_places=5)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True)

    road_1_distance = models.DecimalField(max_digits=20, decimal_places=5, default=0)
    road_2_distance = models.DecimalField(max_digits=20, decimal_places=5, default=0)
    road_3_distance = models.DecimalField(max_digits=20, decimal_places=5, default=0)

    road_1_amount = models.DecimalField(max_digits=20, decimal_places=5, default=0)
    road_2_amount = models.DecimalField(max_digits=20, decimal_places=5, default=0)
    road_3_amount = models.DecimalField(max_digits=20, decimal_places=5, default=0)
    # Amount in the lowest denomination (paisa)
    amount = models.DecimalField(max_digits=20, decimal_places=5, default=0)

    part_name = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    @property
    def amount_rs(self):
        return self.amount / 100

    @property
    def transportation_rate(self):
        return (
            self.road_1_distance * self.road_1_amount
            + self.road_2_distance * self.road_2_amount
            + self.road_3_distance * self.road_3_amount
        )

    @property
    def total_rate(self):
        return self.transportation_rate + self.amount


class Quantity(BaseModel):
    quantity_type_choices = (
        ("DIAMETER", "Diameter"),
        ("DEFAULT", "Default"),
    )

    quantity_type = models.CharField(
        max_length=255, default="DEFAULT", choices=quantity_type_choices
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, null=True, related_name="estimation_rates"
    )
    type_choices = (
        ("PART", "Part"),
        ("SUB_PART", "Sub Part"),
        ("TOPIC", "Topic"),
        ("SUB_TOPIC", "Sub Topic"),
        ("ITEM", "Item"),
        ("TOTAL", "Total"),
    )
    type = models.CharField(choices=type_choices, null=True, blank=True, max_length=20)
    norm = models.ForeignKey(
        "norm.Norm", null=True, blank=True, on_delete=models.PROTECT
    )

    partid = models.CharField(max_length=255, null=True, blank=True)
    subpartid = models.CharField(max_length=255, null=True, blank=True, default="0")
    itemid = models.CharField(max_length=255, null=True, blank=True, default="0")
    topicid = models.CharField(max_length=255, null=True, blank=True, default="0")
    subtopicid = models.CharField(max_length=255, null=True, blank=True, default="0")
    is_leaf = models.BooleanField(blank=True, null=True, default=False)
    provisional = models.BooleanField(blank=True, null=True, default=False)

    line_number = models.CharField(max_length=250, null=True, blank=True)
    s_no = models.CharField(max_length=250, null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    no = models.DecimalField(
        max_digits=20, decimal_places=5, null=True, blank=True, default="0.0"
    )
    length = models.DecimalField(
        max_digits=20, decimal_places=5, null=True, blank=True, default="0.0"
    )
    breadth = models.DecimalField(
        max_digits=20, decimal_places=5, null=True, blank=True, default="0.0"
    )
    height = models.DecimalField(
        max_digits=20, decimal_places=5, null=True, blank=True, default="0.0"
    )
    area = models.DecimalField(
        max_digits=20, decimal_places=5, null=True, blank=True, default="0.0"
    )
    quantity = models.DecimalField(
        max_digits=20, decimal_places=5, null=True, blank=True, default="0.0"
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return f"{self.type}----{self.s_no}"

    def save(self, *args, **kwargs):
        if self.quantity_type == "DIAMETER":
            self.height = self.breadth**2 / 162
            self.quantity = self.no * self.length * self.height
        super().save(*args, **kwargs)

    @property
    def has_children(self):
        return self.children.exists()

    @property
    def total_quantities_dict(self):
        total_dict = {}
        (
            total_dict["total_no"],
            total_dict["total_length"],
            total_dict["total_breadth"],
            total_dict["total_height"],
            total_dict["total_quantity"],
        ) = self.total_quantities
        return total_dict

    @property
    def total_quantities(self):
        if not self.has_children:
            return (
                float(self.no or 0),
                float(self.length or 0),
                float(self.breadth or 0),
                float(self.height or 0),
                float(self.quantity or 0),
            )
        total_no, total_length, total_breadth, total_height, total_quantity = (
            0,
            0,
            0,
            0,
            0,
        )
        for child in self.children.all():
            no, length, breadth, height, quantity = child.total_quantities
            total_no += no
            total_length += length
            total_breadth += breadth
            total_height += height
            total_quantity += quantity
        return total_no, total_length, total_breadth, total_height, total_quantity

    class Meta:
        verbose_name_plural = "Quantities"


class SummaryExtra(BaseModel):
    s_no = models.CharField(blank=True, max_length=255)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True)
    description = models.TextField(blank=True)
    amount = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, default="0.0"
    )
    rate = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, default="0.0"
    )
    remarks = models.TextField(blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
