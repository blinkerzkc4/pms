from django.db import models
from django.utils.translation import gettext_lazy as _

from base_model.choices import VerificationStatusChoices
from project.models import BaseModel, District, Municipality, Province, Ward

# Create your models here.


class CommonFieldsBase(BaseModel):
    code = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name=_("Code"),
        help_text="कोड",
    )
    name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Name"), help_text="नाम"
    )
    name_eng = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Name (Eng)"),
        help_text="नाम (अंग्रेजी)",
    )
    detail = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_("Detail"),
        help_text="विवरण",
    )
    verfication_status = models.CharField(
        max_length=55,
        help_text="सत्यापन स्थिति",
        verbose_name=_("Verification Status"),
        choices=VerificationStatusChoices.choices,
        default=VerificationStatusChoices.na,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"Code: {self.code}, ID: {self.id}"


class Gender(CommonFieldsBase):
    def __str__(self):
        return str(self.name or self.name_eng or self.id)


class Address(BaseModel):
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
    village_name = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Village Name",
        help_text="गाउँको नाम",
    )
    road_name = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Road Name",
        help_text="सडकको नाम",
    )
    road_name_eng = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Road Name (Eng)",
        help_text="सडकको नाम (अंग्रेजी)",
    )

    def __str__(self):
        if self.municipality:
            return f"{self.municipality}-{self.ward}, {self.municipality.district}"
        else:
            return str(self.id)


class ContactDetail(BaseModel):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    fax_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mailing_address = models.CharField(max_length=250, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)


class ContactPerson(BaseModel):
    name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Name", help_text="नाम"
    )
    name_eng = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Name (Eng)",
        help_text="नाम (अंग्रेजी)",
    )
    position = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Position", help_text="पद"
    )
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Phone Number",
        help_text="फोन नं",
    )
    mobile_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Mobile Number",
        help_text="मोबाइल नं",
    )
    email = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Email", help_text="ईमेल"
    )
    remark = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Remark",
        help_text="कैफियत",
    )
    kramagat = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Kramagat",
        help_text="क्रमागत",
    )


class DocumentType(BaseModel):
    code = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    name_eng = models.CharField(max_length=255, null=True, blank=True)
    detail = models.CharField(max_length=255, null=True, blank=True)
    document_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.document_type}"
