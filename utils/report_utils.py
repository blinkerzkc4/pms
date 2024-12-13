from typing import List, Set, TypedDict

from utils.search import search_list_of_dicts

IGNORE_FIELDS = [
    "id",
    "created_date",
    "updated_date",
    "created_by",
    "updated_by",
    "status",
    # Parent classes fields
    "parent",
    # User Fields
    "groups",
    "user_permissions",
    "last_login",
    "is_superuser",
    "is_staff",
    "is_active",
    "password",
    "detail",
    "verified",
    "kramagat",
    "remarks",
    "print_custom_report",
    "image",
]

MODELS_TO_IGNORE = [
    "UserRole",
    "Permission",
    "Group",
    "ProjectExecutionDocument",
    "ProjectUnitDetail",
]

RELATED_MODEL_TO_IGNORE = {
    "project": "ProjectExecution",
}

SHOW_RELATION_NAME_ONLY = [
    "Municipality",
    "District",
    "Province",
    "SubjectArea",
    "ProjectNature",
    "ProjectType",
    "StrategicSign",
    "Program",
    "PriorityType",
    "StartPmsProcess",
    "PlanStartDecision",
    "Unit",
    "Currency",
    "Module",
    "ProjectAddress" "SubModule",
    "NewsPaper",
    "ProjectStartDecision",
    "ConstructionMaterialDescription",
    "BudgetSubTitle",
    "PaymentMethod",
    "SourceReceipt",
    "CollectPayment",
    "SubLedger",
    "OrganizationType",
    "ContractorType",
    "ProjectStatus",
    "TargetGroupCategory",
    "SelectionFeasibility",
    "PurchaseType",
    "ProjectActivity",
]

RELATED_MODELS_NAMES = {
    "ConsumerCommittee": ["consumer_committee", "user_committee"],
}


class ModelFieldsDict(TypedDict):
    type: str
    name: str
    verbose_name: str
    description: str
    help_text: str
    related_model_fields: List["ModelFieldsDict"]


def should_ignore_model(field, model):
    return (
        model.__name__ in MODELS_TO_IGNORE
        or RELATED_MODEL_TO_IGNORE.get(field.name) == model.__name__
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


def get_model_fields_old(
    model, already_included_models: Set[str] = None, should_repeat_models: bool = True
):
    fields_list = []
    if already_included_models is None:
        already_included_models = {model.__name__}
    related_model_fields_dictionary = (
        {}
    )  # Store related model fields to avoid duplicate recursive calls
    for field in model._meta.get_fields():
        if should_ignore_field(field.name):
            continue  # Ignore fields
        if hasattr(field, "value_from_object"):
            field_info = {
                "type": "relation" if field.is_relation else "field",
                "name": str(field.name),
                "verbose_name": str(field.verbose_name),
                "description": str(field.description),
                "help_text": str(field.help_text),
            }
            if field.is_relation:
                if (
                    not should_repeat_models
                    and field.related_model.__name__ in already_included_models
                ):
                    continue
                already_included_models.add(field.related_model.__name__)
                if should_ignore_model(field, field.related_model):
                    continue  # Ignore models
                elif field.related_model.__name__ == model.__name__:
                    continue  # Ignore self relation
                elif show_relation_name_only(field.related_model):
                    field_info["related_model_fields"] = [
                        {
                            "type": "relation"
                            if related_model_field.is_relation
                            else "field",
                            "name": str(related_model_field.name),
                            "verbose_name": str(related_model_field.verbose_name),
                            "description": str(related_model_field.description),
                            "help_text": str(related_model_field.help_text),
                        }
                        for related_model_field in field.related_model._meta.get_fields()
                        if "name" in str(related_model_field.name)
                    ]
                else:
                    if not related_model_fields_dictionary.get(field.related_model):
                        fields, already_included_models = get_model_fields_old(
                            field.related_model,
                            already_included_models=already_included_models,
                            should_repeat_models=should_repeat_models,
                        )  # Recursive call to get related model fields
                        related_model_fields_dictionary[field.related_model] = fields
                    field_info[
                        "related_model_fields"
                    ] = related_model_fields_dictionary.get(field.related_model)
            fields_list.append(field_info)
    return fields_list, already_included_models


def get_model_fields(
    model, already_included_models: Set[str] = None, should_repeat_models: bool = True
):
    fields_list = []
    if already_included_models is None:
        already_included_models = {model.__name__}
    related_model_fields_dictionary = (
        {}
    )  # Store related model fields to avoid duplicate recursive calls
    for field in model._meta.get_fields():
        field_info = {}
        if should_ignore_field(field.name):
            continue  # Ignore fields
        if hasattr(field, "value_from_object"):
            field_model = field.related_model if field.is_relation else model
            model_code = "".join(
                [word[0] for word in field_model._meta.verbose_name.lower().split(" ")]
            )
            field_info = {
                "type": "relation:one_to_one" if field.is_relation else "field",
                "name": str(field.name),
                "model": {
                    "name": field_model.__name__,
                    "app_label": field_model._meta.app_label,
                    "verbose_name": field_model._meta.verbose_name,
                    "code": model_code,
                    "related_field_name": str(field.name)
                    if field.is_relation
                    else None,
                },
                "verbose_name": str(field.verbose_name),
                "description": str(field.description),
                "help_text": str(field.help_text),
            }
            if field.is_relation:
                if (
                    not should_repeat_models
                    and field.related_model.__name__ in already_included_models
                ):
                    continue
                already_included_models.add(field.related_model.__name__)
                if should_ignore_model(field, field.related_model):
                    continue  # Ignore models
                elif field.related_model.__name__ == model.__name__:
                    continue  # Ignore self relation
                elif show_relation_name_only(field.related_model):
                    field_info["related_model_fields"] = [
                        # {
                        #     "type": "relation"
                        #     if related_model_field.is_relation
                        #     else "field",
                        #     "name": str(related_model_field.name),
                        #     "verbose_name": str(related_model_field.verbose_name),
                        #     "description": str(related_model_field.description),
                        #     "help_text": str(related_model_field.help_text),
                        # }
                        # for related_model_field in field.related_model._meta.get_fields()
                        # if "name" in str(related_model_field.name)
                    ]
                else:
                    if not related_model_fields_dictionary.get(field.related_model):
                        fields, already_included_models = get_model_fields(
                            field.related_model,
                            already_included_models=already_included_models,
                            should_repeat_models=should_repeat_models,
                        )  # Recursive call to get related model fields
                        related_model_fields_dictionary[field.related_model] = fields
                    field_info[
                        "related_model_fields"
                    ] = related_model_fields_dictionary.get(field.related_model)
        if field.many_to_many:
            continue
            field_info = {
                "type": "relation:many_to_many",
                "name": str(field.name),
                "model": str(field.related_model.__name__),
                "verbose_name": "",
                "description": "",
                "help_text": "",
            }
            if (
                not should_repeat_models
                and field.related_model.__name__ in already_included_models
            ):
                continue
            already_included_models.add(field.related_model.__name__)
            if should_ignore_model(field, field.related_model):
                continue
        if field_info:
            fields_list.append(field_info)
    return fields_list, already_included_models


def create_crt_field_names(
    starting_crt_field: dict,
    model_fields: list[dict],
    ignore_field_codes=None,
    initial_crt_model_names: list[str] = None,
    parent_model: str = None,
) -> list[dict]:
    if ignore_field_codes is None:
        ignore_field_codes = []
    if initial_crt_model_names is None:
        initial_crt_model_names = []
    crt_fields = []
    for field in model_fields:
        initial_crt_field = starting_crt_field.get("initial_crt_field", False) or (
            field.get("model", {}).get("name", "") in initial_crt_model_names
        )
        crt_field = {
            "code": f"{starting_crt_field['code']}.{field['name']}",
            "type": field["type"],
            "model_field": field["name"]
            if initial_crt_field
            else f"{starting_crt_field.get('model_field')}.{field['name']}",
            "parent_model": parent_model,
            "name": f"{starting_crt_field['name']} > {field['help_text']}",
            "name_eng": f"{starting_crt_field['name_eng']} > {field['verbose_name']}",
            "help_text": field["help_text"],
        }
        if field.get("model"):
            if parent_model:
                if field["model"]["related_field_name"]:
                    if parent_model.get("related_field_name"):
                        field["model"]["related_field_name"] += parent_model.get(
                            "related_field_name"
                        )
                else:
                    field["model"]["related_field_name"] = parent_model.get(
                        "related_field_name"
                    )
            crt_field["model"] = field["model"]
        if field["type"] == "field":
            if crt_field["code"] in ignore_field_codes:
                continue
            crt_fields.append(crt_field)
        else:
            crt_fields.extend(
                create_crt_field_names(
                    crt_field,
                    field["related_model_fields"],
                    ignore_field_codes=ignore_field_codes,
                    initial_crt_model_names=initial_crt_model_names,
                    parent_model=starting_crt_field["model"]
                    if field["type"] == "relation:one_to_one"
                    else None,
                )
            )
    return crt_fields


DONT_COMBINE_CRT_MODELS = ["Employee"]


def should_combine_crt_field(crt_field_dict):
    return crt_field_dict["model"]["name"] not in DONT_COMBINE_CRT_MODELS


def group_crt_fields(crt_fields: list[dict]) -> list[dict]:
    grouped_crt_fields = []
    for crt_field in crt_fields:
        dict_key = f"{crt_field['parent_model']}{crt_field['model']} {crt_field['model_field']}"
        if crt_field["parent_model"]:
            related_model_names = RELATED_MODELS_NAMES.get(
                crt_field["parent_model"]["name"]
            )
            if related_model_names:
                for related_model_name in related_model_names[1:]:
                    dict_key = dict_key.replace(
                        related_model_name, related_model_names[0]
                    )
        crt_field_dict = search_list_of_dicts(grouped_crt_fields, "code", dict_key)
        if crt_field_dict and should_combine_crt_field(crt_field_dict):
            crt_field_index = grouped_crt_fields.index(crt_field_dict)
            crt_field_dict["db_columns"].append(crt_field["code"])
            grouped_crt_fields[crt_field_index] = crt_field_dict
        else:
            if should_combine_crt_field(crt_field):
                # report_code = f"{crt_field['parent_model']['code']}_{crt_field['model']['code']}_{crt_field['model_field']}"
                report_code = (
                    crt_field["parent_model"]["code"]
                    if crt_field["parent_model"]
                    else "" + "_" + crt_field["parent_model"]["related_field_name"]
                    if crt_field["parent_model"]
                    else crt_field["model"]["name"] + "_" + crt_field["model_field"]
                )
            else:
                report_code = f"{crt_field['model']['name']}_{crt_field['model_field']}"
            grouped_crt_field = {
                "model": crt_field["model"],
                "db_field_type": crt_field["type"],
                "parent_model": crt_field["parent_model"],
                "model_field": crt_field["model_field"],
                "name": crt_field["name"],
                "name_eng": crt_field["name_eng"],
                "help_text": crt_field["help_text"],
                "code": dict_key,
                "report_code": report_code,
                "db_columns": [
                    crt_field["code"],
                ],
            }
            grouped_crt_fields.append(grouped_crt_field)
    return grouped_crt_fields


def get_model_field(model, field_name):
    field = model._meta.get_field(field_name)
    return field


def get_field_value_from_object_old(obj, field_name, sub_field_name=None):
    field = obj._meta.get_field(field_name)
    value = field.value_from_object(obj)
    # if field.is_relation and value and str(field) not in SHOW_RELATION_NAME_ONLY:
    #     if field.many_to_many:
    #         value = [i.id for i in value.all()]
    #     else:
    #         value = field.related_model.objects.get(pk=value)
    return value


def get_field_value_from_object(obj, field_names: list[str]):
    field_name = field_names.pop(0)
    field = obj._meta.get_field(field_name)
    value = field.value_from_object(obj)
    if field.is_relation:
        if value is None:
            return value
        if show_relation_name_only(field.related_model):
            value = str(
                get_field_value_from_object(field.related_model.objects.get(pk=value))
            )
        elif len(field_names) > 0 and value is not None:
            value = get_field_value_from_object(
                field.related_model.objects.get(pk=value), field_names
            )
    return value
