import json
from typing import List

from app_settings.datatypes import SettingJsonDict
from app_settings.models import AppSettingCollection


class Setting:
    def __init__(self) -> None:
        pass

    @classmethod
    def open_setting(cls, municipality, request=None):
        app_setting_collection = AppSettingCollection.objects.get(
            municipality=municipality
        )

        with open(
            "app_settings/data/general_settings.json", "r", encoding="utf-8"
        ) as general_settings_json:
            general_settings: List[SettingJsonDict] = json.load(general_settings_json)

        setting_obj = cls()

        for setting in general_settings:
            if setting["value_type"] == "image":
                app_setting = app_setting_collection.image_app_settings
                code = setting["code"]
                value = app_setting.get(code=setting["code"]).setting_value
            elif setting["value_type"] == "boolean":
                app_setting = app_setting_collection.boolean_app_settings
                code = setting["code"]
                value = app_setting.get(code=setting["code"]).setting_value
            setattr(
                setting_obj,
                code,
                value,
            )

        return setting_obj
