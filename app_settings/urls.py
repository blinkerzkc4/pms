from django.urls import path

from app_settings.views import (
    AppSettingCollectionView,
    BooleanAppSettingUpdateView,
    EnumAppSettingUpdateView,
    FloatAppSettingUpdateView,
    ImageAppSettingUpdateView,
    IntegerAppSettingUpdateView,
    TextAppSettingUpdateView,
)

app_name = "app_settings"
urlpatterns = [
    path(
        "settings/",
        AppSettingCollectionView.as_view(),
        name="settings",
    ),
    path(
        "settings/boolean/<int:app_setting_id>/",
        BooleanAppSettingUpdateView.as_view(),
        name="update-boolean",
    ),
    path(
        "settings/image/<int:app_setting_id>/",
        ImageAppSettingUpdateView.as_view(),
        name="update-image",
    ),
    path(
        "settings/integer/<int:app_setting_id>/",
        IntegerAppSettingUpdateView.as_view(),
        name="update-integer",
    ),
    path(
        "settings/text/<int:app_setting_id>/",
        TextAppSettingUpdateView.as_view(),
        name="update-text",
    ),
    path(
        "settings/enum/<int:app_setting_id>/",
        EnumAppSettingUpdateView.as_view(),
        name="update-enum",
    ),
    path(
        "settings/float/<int:app_setting_id>/",
        FloatAppSettingUpdateView.as_view(),
        name="update-float",
    ),
]
