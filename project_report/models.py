from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from base_model.models import CommonFieldsBase, DocumentType
from project.models import BaseModel
from project_report.choices import FieldTypeChoices
from project_report.validators import validate_template_content
from utils.constants import ORIENTATION_CHOICES


class TemplateFieldMappingGroup(CommonFieldsBase):
    def __str__(self):
        return self.name if self.name else str(self.id)


class TemplateFieldMapping(CommonFieldsBase):
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(
        "user.User",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="deleted_template_field_mappings",
    )
    deleted_on = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(
        "user.User",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="updated_template_field_mappings",
    )
    group = models.ForeignKey(
        TemplateFieldMappingGroup,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="template_field_mappings",
    )
    display_name = models.CharField(max_length=255, null=True, blank=True)
    display_name_eng = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, unique=True)
    field_type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=FieldTypeChoices.choices,
        default=FieldTypeChoices.DB_COLUMN,
    )
    db_column_names = ArrayField(
        models.CharField(max_length=255, null=True, blank=True), null=True, blank=True
    )
    report_code = models.TextField(
        null=True,
        blank=True,
    )
    name = models.TextField(null=True, blank=True)
    name_eng = models.TextField(null=True, blank=True)
    pms_process_id = models.ForeignKey(
        "plan_execution.StartPmsProcess",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="सञ्चालन प्रकृया",
    )
    client_ward = models.IntegerField(null=True, blank=True)
    client_id = models.ForeignKey(
        "user.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="client_user",
    )
    process_name = models.CharField(max_length=100, null=True, blank=True)
    db_column_name = models.CharField(max_length=255, null=True, blank=True)
    default_value = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True, help_text="कैफियत")
    status = models.BooleanField(default=True, null=True, blank=True)

    @property
    def code_only(self):
        return self.code.split("|")[0]

    @property
    def report_code_for_template(self):
        if self.field_type == FieldTypeChoices.LOOP:
            return f"{{% autoescape off %}}{self.report_code}{{% endautoescape %}}"
        else:
            return self.code

    def __str__(self):
        return self.name if self.name else str(self.id)


class ReportType(CommonFieldsBase):
    code = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name if self.name else str(self.id)


class CustomReportTemplate(BaseModel):
    client_id = models.ForeignKey(
        "user.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="template_client",
    )
    template_type_id = models.ForeignKey(
        ReportType, null=True, blank=True, on_delete=models.PROTECT
    )
    is_template_default = models.BooleanField(default=True)
    plan_master_id = models.ForeignKey(
        "user.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="template_plan_master",
    )
    name_eng = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    orientation = models.CharField(
        max_length=10, choices=ORIENTATION_CHOICES, null=True, blank=True
    )
    required_renders = models.PositiveIntegerField(default=1, null=True, blank=True)
    template_content = models.TextField(
        null=True, blank=True, validators=[validate_template_content]
    )
    template_info = models.CharField(max_length=255, null=True, blank=True)
    client_ward = models.IntegerField(null=True, blank=True)
    is_report_header_show = models.BooleanField(default=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    start_pms_process = models.ForeignKey(
        "plan_execution.StartPmsProcess",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text="सञ्चालन प्रकृया",
    )
    is_ward_template = models.BooleanField(default=False)
    is_new_template = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.template_type_id}"
            if self.name is not None
            else str(self.id)
        )


@receiver(post_save, sender=ReportType)
def report_type_post_save_receiver(sender, instance, created, **kwargs):
    print("report_type_post_save_receiver")
    if created:
        print("Creating new document")
        DocumentType.objects.create(
            name=instance.name,
            name_eng=instance.name_eng,
            code=instance.code,
            detail=instance.detail,
            document_type="report_type",
        )
