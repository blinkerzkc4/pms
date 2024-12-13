import json

from django.apps import apps as django_apps

from project_report.constants.models_for_crt import CRT_MODELS_LIST
from utils.report.model_fields import get_model_fields


def refresh_data() -> None:
    """Refreshes the data in data/report/ directory with the latest model fields."""
    already_included_models = set()
    for crt_model in CRT_MODELS_LIST:
        model = django_apps.get_model(
            app_label=crt_model["app_name"], model_name=crt_model["model"]
        )

        fields, already_included_models = get_model_fields(
            model,
            already_included_models=already_included_models,
            # should_repeat_models=False,
        )

        with open(
            f"data/report/model_fields/{crt_model['app_name']}_{crt_model['model']}_fields.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(fields, f, indent=4)
