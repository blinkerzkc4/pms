import json
from typing import List

from django.db.models.signals import post_save
from django.dispatch import receiver

from app_settings.choices import AppSettingType
from app_settings.datatypes import SettingJsonDict
from app_settings.models import AppSettingCollection
from app_settings.utils.constants import SETTING_TYPE_MODEL_MAPPING


@receiver(post_save, sender=AppSettingCollection)
def create_individual_app_settings(sender, instance, created, **kwargs):
    with open(
        "app_settings/data/general_settings.json", "r", encoding="utf-8"
    ) as general_settings_json:
        general_settings: List[SettingJsonDict] = json.load(general_settings_json)
    with open(
        "app_settings/data/yojana_settings.json", "r", encoding="utf-8"
    ) as yojana_settings_json:
        yojana_settings: List[SettingJsonDict] = json.load(yojana_settings_json)
    with open(
        "app_settings/data/report_settings.json", "r", encoding="utf-8"
    ) as report_settings_json:
        report_settings: List[SettingJsonDict] = json.load(report_settings_json)
    if created:
        for setting in general_settings:
            value_type = setting.pop("value_type")
            delete_this = setting.pop("delete_this", False)
            if delete_this:
                continue
            setting["setting_collection"] = instance
            if SETTING_TYPE_MODEL_MAPPING.get(value_type):
                SETTING_TYPE_MODEL_MAPPING.get(value_type).objects.create(**setting)
        for setting in yojana_settings:
            value_type = setting.pop("value_type")
            delete_this = setting.pop("delete_this", False)
            if delete_this:
                continue
            setting["setting_collection"] = instance
            setting["setting_type"] = AppSettingType.YOJANA
            if SETTING_TYPE_MODEL_MAPPING.get(value_type):
                SETTING_TYPE_MODEL_MAPPING.get(value_type).objects.create(**setting)
        for setting in report_settings:
            value_type = setting.pop("value_type")
            delete_this = setting.pop("delete_this", False)
            if delete_this:
                continue
            setting["setting_collection"] = instance
            setting["setting_type"] = AppSettingType.REPORT
            if SETTING_TYPE_MODEL_MAPPING.get(value_type):
                SETTING_TYPE_MODEL_MAPPING.get(value_type).objects.create(**setting)
