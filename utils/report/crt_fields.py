import json
import os
from dataclasses import field
from typing import List

from utils.report.constants import DONT_COMBINE_CRT_MODELS, RELATED_MODELS_NAMES
from utils.report.datatypes import CustomReportTemplateField, Model, ModelField


def generate_crt_field_names(
    starting_crt_field: CustomReportTemplateField,
    model_fields: List[ModelField],
    ignore_field_codes: List[str] = None,
    initial_crt_model_names: List[str] = None,
    parent_model: Model = None,
) -> List[CustomReportTemplateField]:
    """Generates CRT Fields for the given model fields

    Args:
        starting_crt_field (CustomReportTemplateField): Starting CRT Field for the model fields
        model_fields (List[ModelField]): Model fields for which the CRT Fields are to be generated
        ignore_field_codes (List[str], optional): Field codes to ignore in the CRT fields list. Defaults to None.
        initial_crt_model_names (List[str], optional): Names of the starting models for the CRT Fields. Defaults to empty list.
        parent_model (Model, optional): Parent model of the model of the CRT Field in case of a relation. Defaults to None.

    Returns:
        List[CustomReportTemplateField]: List of CRT Fields generated for the given model fields
    """

    # Seting default values to empty list
    ignore_field_codes = ignore_field_codes or []
    initial_crt_model_names = initial_crt_model_names or []
    crt_fields: List[CustomReportTemplateField] = []

    for model_field in model_fields:
        is_initial_crt_field: bool = (
            starting_crt_field.get("is_initial_crt_field", False)
            or model_field.get("model", {}).get("name") in initial_crt_model_names
        )
        model_field_name = (
            model_field["name"]
            if is_initial_crt_field
            else f"{starting_crt_field['model_field']}.{model_field['name']}"
        )

        # Getting all the related models for the CRT Field
        all_related_models = starting_crt_field.get("all_related_models") or []
        new_all_related_models = (
            all_related_models.copy()
        )  # copying the list to avoid mutation
        if len(new_all_related_models) == 0:
            new_all_related_models.append(starting_crt_field["model"])
        if parent_model:
            new_all_related_models.append(parent_model)

        # Construting the crt field
        crt_field: CustomReportTemplateField = {
            "code": f"{starting_crt_field['code']}.{model_field['name']}",
            "type": model_field["type"],
            "model_field": model_field_name,
            "name": f"{starting_crt_field['name']}>{model_field['help_text']}",
            "name_eng": f"{starting_crt_field['name_eng']}>{model_field['verbose_name']}",
            "model": model_field.get("model"),
            "parent_model": parent_model,
            "db_column": f"{starting_crt_field['code']}.{model_field['name']}",
            "all_related_models": new_all_related_models,
        }
        if model_field["type"] == "field":
            if crt_field["code"] not in ignore_field_codes:
                crt_fields.append(crt_field)
        else:
            # Recursively generating crt fields for the related model fields
            crt_fields.extend(
                generate_crt_field_names(
                    starting_crt_field=crt_field,
                    model_fields=model_field["related_model_fields"],
                    ignore_field_codes=ignore_field_codes,
                    initial_crt_model_names=initial_crt_model_names,
                    parent_model=model_field["model"],
                )
            )
    return crt_fields


def generate_crt_fields_from_data():
    MODEL_FIELDS_DIR = "data\\report\\model_fields"
    filenames_list = os.listdir(MODEL_FIELDS_DIR)

    all_crt_fields = []
    for filename in filenames_list:
        filepath = os.path.join(MODEL_FIELDS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as model_fields_file:
            model_fields = json.load(model_fields_file)
