DONT_COMBINE_CRT_MODELS = ["Employee"]

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
]

RELATED_MODEL_TO_IGNORE = {
    "project": "ProjectExecution",
}

DO_NOT_IGNORE_MODEL = [
    "Project",
]

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
    "SubModule",
    "NewsPaper",
    "ProjectStartDecision",
    "ConstructionMaterialDescription",
    "BudgetSubTitle",
    "PaymentMethod",
    "SourceReceipt",
    "CollectPayment",
    "SubLedger",
    "Address",
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
