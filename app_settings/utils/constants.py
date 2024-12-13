from app_settings.models import (
    BooleanAppSetting,
    EnumAppSetting,
    FloatAppSetting,
    ImageAppSetting,
    IntegerAppSetting,
    TextAppSetting,
)

SETTING_TYPE_MODEL_MAPPING = {
    "image": ImageAppSetting,
    "boolean": BooleanAppSetting,
    "integer": IntegerAppSetting,
    "float": FloatAppSetting,
    "enum": EnumAppSetting,
    "text": TextAppSetting,
}
