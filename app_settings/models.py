from django.apps import apps as django_apps
from django.db import models

from app_settings.choices import (
    AppSettingFunctionChoices,
    AppSettingType,
    AppSettingValueTypeChoices,
)
from project.models import BaseModel
from utils.report_utils import get_field_value_from_object


# Create your models here.
class AppSetting(BaseModel):
    setting_type = models.CharField(
        max_length=55,
        verbose_name="Setting Type",
        help_text="सेटिङ्ग प्रकार",
        choices=AppSettingType.choices,
        default=AppSettingType.GENERAL,
    )
    setting_function = models.CharField(
        max_length=55,
        verbose_name="Setting Function",
        help_text="सेटिङ्ग कार्य",
        choices=AppSettingFunctionChoices.choices,
        default=AppSettingFunctionChoices.LOCAL_VALUE,
    )
    code = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Code",
        help_text="कोड",
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Name",
        help_text="नाम",
    )
    name_eng = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Name (Eng)",
        help_text="नाम (अंग्रेजी)",
    )
    use_in_report = models.BooleanField(
        default=False,
        verbose_name="Use in Report",
        help_text="रिपोर्टमा प्रयोग गर्नुहोस्",
    )
    in_app_model = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="In App Model",
        help_text="एप मा मोडेल",
    )
    in_app_model_field = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="In App Model Field",
        help_text="एप मा मोडेल फिल्ड",
    )
    in_app_municipality_id_field = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="In App Municipality Field",
        help_text="एप मा नगरपालिका फिल्ड",
    )

    @property
    def setting_model(self):
        return (
            None if not self.in_app_model else django_apps.get_model(self.in_app_model)
        )

    @property
    def setting_model_obj(self):
        return (
            None
            if not self.setting_model
            else self.setting_model.objects.filter(
                **{
                    self.in_app_municipality_id_field: self.setting_collection.municipality.id
                }
            ).first()
        )

    def save(self, *args, **kwargs):
        if self.setting_function == AppSettingFunctionChoices.LOCAL_VALUE:
            self.in_app_model = None
            self.in_app_model_field = None
            self.in_app_municipality_id_field = None
        else:
            self.value = get_field_value_from_object(
                self.setting_model_obj, self.in_app_model_field.split(".")
            )
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class BooleanAppSetting(AppSetting):
    value = models.BooleanField(
        default=False,
        verbose_name="Value",
        help_text="मान",
    )
    value_type = models.CharField(
        max_length=55,
        verbose_name="Value Type",
        help_text="मान प्रकार",
        choices=AppSettingValueTypeChoices.choices,
        default=AppSettingValueTypeChoices.BOOLEAN,
        editable=False,
    )
    setting_collection = models.ForeignKey(
        "app_settings.AppSettingCollection",
        on_delete=models.CASCADE,
        related_name="boolean_app_settings",
        verbose_name="Setting Collection",
        help_text="सेटिङ्ग संग्रह",
    )

    @property
    def setting_value(self):
        return self.value

    class Meta:
        verbose_name = "Boolean App Setting"
        verbose_name_plural = "Boolean App Settings"

    def __str__(self):
        return str(self.id)


class IntegerAppSetting(AppSetting):
    value = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Value",
        help_text="मान",
    )
    value_type = models.CharField(
        max_length=55,
        verbose_name="Value Type",
        help_text="मान प्रकार",
        choices=AppSettingValueTypeChoices.choices,
        default=AppSettingValueTypeChoices.INTEGER,
        editable=False,
    )
    setting_collection = models.ForeignKey(
        "app_settings.AppSettingCollection",
        on_delete=models.CASCADE,
        related_name="integer_app_settings",
        verbose_name="Setting Collection",
        help_text="सेटिङ्ग संग्रह",
    )

    @property
    def setting_value(self):
        return self.value

    class Meta:
        verbose_name = "Integer App Setting"
        verbose_name_plural = "Integer App Settings"

    def __str__(self):
        return str(self.id)


class FloatAppSetting(AppSetting):
    value = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Value",
        help_text="मान",
    )
    value_type = models.CharField(
        max_length=55,
        verbose_name="Value Type",
        help_text="मान प्रकार",
        choices=AppSettingValueTypeChoices.choices,
        default=AppSettingValueTypeChoices.FLOAT,
        editable=False,
    )
    setting_collection = models.ForeignKey(
        "app_settings.AppSettingCollection",
        on_delete=models.CASCADE,
        related_name="float_app_settings",
        verbose_name="Setting Collection",
        help_text="सेटिङ्ग संग्रह",
    )

    @property
    def setting_value(self):
        return self.value

    class Meta:
        verbose_name = "Float App Setting"
        verbose_name_plural = "Float App Settings"

    def __str__(self):
        return str(self.id)


class TextAppSetting(AppSetting):
    value = models.CharField(
        null=True,
        blank=True,
        verbose_name="Value",
        help_text="मान",
    )
    value_type = models.CharField(
        max_length=55,
        verbose_name="Value Type",
        help_text="मान प्रकार",
        choices=AppSettingValueTypeChoices.choices,
        default=AppSettingValueTypeChoices.TEXT,
        editable=False,
    )
    setting_collection = models.ForeignKey(
        "app_settings.AppSettingCollection",
        on_delete=models.CASCADE,
        related_name="text_app_settings",
        verbose_name="Setting Collection",
        help_text="सेटिङ्ग संग्रह",
    )

    @property
    def setting_value(self):
        return self.value

    class Meta:
        verbose_name = "Text App Setting"
        verbose_name_plural = "Text App Settings"

    def __str__(self):
        return str(self.id)


class ImageAppSetting(AppSetting):
    value = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Value",
        help_text="मान",
    )
    setting_collection = models.ForeignKey(
        "app_settings.AppSettingCollection",
        on_delete=models.CASCADE,
        verbose_name="Setting Collection",
        help_text="सेटिङ्ग संग्रह",
        related_name="image_app_settings",
    )
    value_type = models.CharField(
        max_length=55,
        verbose_name="Value Type",
        help_text="मान प्रकार",
        choices=AppSettingValueTypeChoices.choices,
        default=AppSettingValueTypeChoices.IMAGE,
        editable=False,
    )

    @property
    def setting_value(self):
        return self.value.url if self.value else None

    class Meta:
        verbose_name = "Image App Setting"
        verbose_name_plural = "Image App Settings"

    def __str__(self):
        return str(self.id)


class EnumAppSetting(AppSetting):
    value = models.CharField(
        max_length=55,
        null=True,
        blank=True,
        verbose_name="Value",
        help_text="मान",
    )
    setting_collection = models.ForeignKey(
        "app_settings.AppSettingCollection",
        on_delete=models.CASCADE,
        verbose_name="Setting Collection",
        help_text="सेटिङ्ग संग्रह",
        related_name="enum_app_settings",
    )
    value_type = models.CharField(
        max_length=55,
        verbose_name="Value Type",
        help_text="मान प्रकार",
        choices=AppSettingValueTypeChoices.choices,
        default=AppSettingValueTypeChoices.ENUM,
        editable=False,
    )
    options = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Options",
        help_text="विकल्पहरू",
    )

    @property
    def setting_value(self):
        return self.value

    class Meta:
        verbose_name = "Enum App Setting"
        verbose_name_plural = "Enum App Settings"


class AppSettingCollection(BaseModel):
    municipality = models.OneToOneField(
        "project.Municipality",
        related_name="app_setting_collections",
        on_delete=models.CASCADE,
        verbose_name="Municipality",
        help_text="नगरपालिका",
    )

    class Meta:
        verbose_name = "App Setting Collection"
        verbose_name_plural = "App Setting Collections"

    def __str__(self):
        return f"{self.municipality} App Settings"
