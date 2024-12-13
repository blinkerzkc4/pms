from django.db.models import TextChoices


class AppSettingValueTypeChoices(TextChoices):
    TEXT = "text", "Text"
    INTEGER = "integer", "Integer"
    FLOAT = "float", "Float"
    BOOLEAN = "boolean", "Boolean"
    IMAGE = "image", "Image"
    FILE = "file", "File"
    ENUM = "enum", "Enum"


class AppSettingType(TextChoices):
    GENERAL = "general", "General"
    YOJANA = "yojana", "Yojana"
    REPORT = "report", "Report"


class AppSettingFunctionChoices(TextChoices):
    LOCAL_VALUE = "local_value", "Local Value"
    DB_VALUE = "DB_value", "DB Value"
