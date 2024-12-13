from typing import Set

from django.db.models import Field as DjangoField
from django.db.models import Model as DjangoModel

from utils.report.constants import (
    DO_NOT_IGNORE_MODEL,
    IGNORE_FIELDS,
    MODELS_TO_IGNORE,
    RELATED_MODEL_TO_IGNORE,
    SHOW_RELATION_NAME_ONLY,
)
from utils.report.datatypes import Model, ModelField


def get_field_type(field: DjangoField) -> str:
    if field.is_relation:
        if field.many_to_many:
            return "relation:many_to_many"
        if field.one_to_many:
            return "relation:one_to_many"
        if field.many_to_one:
            return "relation:many_to_one"
        return "relation:one_to_one"
    return "field"


def should_ignore_model(field, model):
    return (
        model.__name__ in MODELS_TO_IGNORE
        or RELATED_MODEL_TO_IGNORE.get(field.name) == model.__name__
        and model.__name__ not in DO_NOT_IGNORE_MODEL
    )


def should_ignore_field(field_name: str):
    return (
        field_name in IGNORE_FIELDS
        or field_name.startswith("is")
        or "token" in field_name
    )


def show_relation_name_only(model):
    non_relation_fields = [
        field.name
        for field in model._meta.get_fields()
        if not field.is_relation and not field.many_to_many
    ]
    return model.__name__ in SHOW_RELATION_NAME_ONLY or len(non_relation_fields) <= 8


def get_model_fields(
    model: DjangoModel,
    already_included_models: Set[str] = None,
    should_repeat_models: bool = True,
):
    fields_list = []
    # Initializing the already_included_models set to set with current model name if not provided
    already_included_models = already_included_models or {model.__name__}
    # Storing the related model fields to avoid duplicate recursive calls
    related_model_fields_dictionary = {}

    for field in model._meta.get_fields():
        field_info: ModelField = {}
        if hasattr(field, "value_from_object"):
            if should_ignore_field(field.name):
                continue
            field_type = get_field_type(field)
            field_model = field.related_model if field.is_relation else model
            model_code = "".join(
                [word[0] for word in field_model._meta.verbose_name.lower().split(" ")]
            )
            field_info = {
                "name": str(field.name),
                "model": {
                    "code": model_code,
                    "name": field_model.__name__,
                    "app_label": field_model._meta.app_label,
                    "verbose_name": field_model._meta.verbose_name,
                    "related_field_name": str(field.name)
                    if field.is_relation
                    else None,
                },
                "type": field_type,
                "verbose_name": str(field.verbose_name),
                "description": str(field.description),
                "help_text": str(field.help_text),
            }
            if field.is_relation:
                if should_ignore_model(field, field_model):
                    continue
                field_info["relation_type"] = field_type
                if show_relation_name_only(field.related_model):
                    field_info["related_model_fields"] = [
                        {
                            "type": "field",
                            "name": str(related_model_field.name),
                            "verbose_name": str(related_model_field.verbose_name),
                            "description": str(related_model_field.description),
                            "help_text": str(related_model_field.help_text),
                        }
                        for related_model_field in field.related_model._meta.get_fields()
                        if "name" in str(related_model_field.name)
                    ]
                else:
                    already_included_models.add(field_model.__name__)
                    related_model_fields = related_model_fields_dictionary.get(
                        field_model.__name__
                    )
                    if not related_model_fields:
                        (
                            related_model_fields,
                            already_included_models,
                        ) = get_model_fields(
                            field_model,
                            already_included_models=already_included_models,
                            should_repeat_models=should_repeat_models,
                        )
                        related_model_fields_dictionary[
                            field_model.__name__
                        ] = related_model_fields
                    field_info["related_model_fields"] = related_model_fields
            if field_info:
                fields_list.append(field_info)

    return fields_list, already_included_models
