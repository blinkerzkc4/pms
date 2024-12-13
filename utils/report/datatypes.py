from typing import List, Optional, TypedDict

# from enum import Enum
# class FieldType(Enum):
#     FIELD = "field"
#     ONE_TO_ONE = "relation:one_to_one"
#     MANY_TO_MANY = "relation:many_to_many"


class Model(TypedDict):
    code: str  # code of the model
    name: str  # name of the model
    app_label: str  # app label of the model
    verbose_name: str  # display name of the model
    related_field_name: str  # name of the related field of the model in the parent model in case of a relation


class ModelField(TypedDict):
    name: str  # name of the model field
    model: Model  # model of the model field
    type: str  # type of the model field
    verbose_name: str  # display name of the model field
    description: str  # description of the model field
    help_text: str  # display name of the model field in nepali
    relation_type: Optional[str]  # type of the crt field's model
    # related model fields of the model field in case of a relation
    related_model_fields: Optional[List["ModelField"]]


class CustomReportTemplateField(TypedDict):
    code: str  # code of the crt field
    type: str  # type of the crt field's model
    model_field: str  # name of the crt field's model field
    name: str  # name of the crt field
    name_eng: str  # name of the crt field in english
    model: Model  # model of the crt field
    parent_model: Model  # parent model of the crt field
    db_column: str  # db column of the crt field
    # whether the crt field is an initial crt field
    is_initial_crt_field: Optional[bool]
    # names of all the related parent models of the crt field
    all_related_models: List[Model]


class GroupedCustomReportTemplateField(CustomReportTemplateField):
    group: str  # group of the crt field
    db_columns: List[str]  # db columns of the crt field
    report_code: str  # report code of the crt field
