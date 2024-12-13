import json
from typing import Any, List

from django.core.management.base import BaseCommand

from app_settings.choices import AppSettingFunctionChoices, AppSettingType
from app_settings.datatypes import SettingJsonDict
from app_settings.models import AppSettingCollection
from app_settings.utils.constants import SETTING_TYPE_MODEL_MAPPING


class Command(BaseCommand):
    help = "Command to update the app settings of the clients."

    def add_arguments(self, parser):
        parser.add_argument(
            "--client_db",
            action="store",
            dest="client_db",
            help="Database to create app settings into.",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        database = options.get("client_db", "default")

        def process_setting(
            value_type, setting_code, app_setting_collection, setting_data
        ):
            delete_setting = setting_data.pop("delete_this", False)
            if delete_setting:
                settings = (
                    SETTING_TYPE_MODEL_MAPPING.get(value_type)
                    .objects.using(database)
                    .filter(
                        code=setting_code, setting_collection=app_setting_collection
                    )
                )
                if settings.exists():
                    settings.delete()
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Deleted {setting_code} for {app_setting_collection.municipality.name_eng}"
                        )
                    )
                return
            setting, setting_created = (
                SETTING_TYPE_MODEL_MAPPING.get(value_type)
                .objects.using(database)
                .update_or_create(
                    code=setting_code,
                    setting_collection=app_setting_collection,
                    defaults=setting_data,
                )
            )
            if setting_created:
                if setting.setting_function == AppSettingFunctionChoices.DB_VALUE:
                    setting.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created {setting_code} for {app_setting_collection.municipality.name_eng}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Updated {setting_code} for {app_setting_collection.municipality.name_eng}"
                    )
                )

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
        for app_setting_collection in AppSettingCollection.objects.using(
            database
        ).all():
            for setting_data in general_settings:
                setting_data = setting_data.copy()
                value_type = setting_data.pop("value_type")
                setting_code = setting_data.pop("code")
                if SETTING_TYPE_MODEL_MAPPING.get(value_type):
                    process_setting(
                        value_type,
                        setting_code,
                        app_setting_collection,
                        setting_data,
                    )
            for setting in yojana_settings:
                setting_data = setting.copy()
                value_type = setting_data.pop("value_type")
                setting_code = setting_data.pop("code")
                setting_data["setting_type"] = AppSettingType.YOJANA
                if SETTING_TYPE_MODEL_MAPPING.get(value_type):
                    process_setting(
                        value_type,
                        setting_code,
                        app_setting_collection,
                        setting_data,
                    )
            for setting in report_settings:
                setting_data = setting.copy()
                value_type = setting_data.pop("value_type")
                setting_code = setting_data.pop("code")
                setting_data["setting_type"] = AppSettingType.REPORT
                if SETTING_TYPE_MODEL_MAPPING.get(value_type):
                    process_setting(
                        value_type,
                        setting_code,
                        app_setting_collection,
                        setting_data,
                    )
