import json

from django.urls import reverse
from rest_framework import serializers

from app_settings.models import (
    AppSetting,
    AppSettingCollection,
    EnumAppSetting,
    FloatAppSetting,
    ImageAppSetting,
    TextAppSetting,
)


class DefaultAppSettingSerializer(serializers.ModelSerializer):
    value_type = serializers.CharField(source="get_value_type_display", read_only=True)
    setting_type = serializers.CharField(read_only=True)
    id = serializers.SerializerMethodField()

    update_link = serializers.SerializerMethodField()

    class Meta:
        model = AppSetting
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "value_type",
            "update_link",
            "setting_type",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "value_type": {"required": False, "allow_null": True},
            "update_link": {"required": False, "allow_null": True},
        }
        update_url_name = ""

    def get_id(self, obj):
        return f"{obj.value_type}-{obj.id}"

    def get_update_link(self, obj):
        # request = self.context.get("request")
        url = reverse(
            self.Meta.update_url_name,
            kwargs={"app_setting_id": obj.id},
        )
        # if request:
        #     url = request.build_absolute_uri(url)
        return url


class BooleanAppSettingSerializer(DefaultAppSettingSerializer):
    value = serializers.BooleanField(
        default=False,
        required=False,
    )

    class Meta(DefaultAppSettingSerializer.Meta):
        model = ImageAppSetting
        fields = DefaultAppSettingSerializer.Meta.fields + ("value",)
        update_url_name = "app_settings:update-boolean"


class IntegerAppSettingSerializer(DefaultAppSettingSerializer):
    value = serializers.IntegerField(
        default=0,
        required=False,
    )

    class Meta(DefaultAppSettingSerializer.Meta):
        model = ImageAppSetting
        fields = DefaultAppSettingSerializer.Meta.fields + ("value",)
        update_url_name = "app_settings:update-integer"


class FloatAppSettingSerializer(DefaultAppSettingSerializer):
    value = serializers.FloatField(
        default=0,
        required=False,
    )

    class Meta(DefaultAppSettingSerializer.Meta):
        model = FloatAppSetting
        fields = DefaultAppSettingSerializer.Meta.fields + ("value",)
        update_url_name = "app_settings:update-float"


class TextAppSettingSerializer(DefaultAppSettingSerializer):
    value = serializers.CharField(
        max_length=255,
        allow_null=True,
        required=False,
    )

    class Meta(DefaultAppSettingSerializer.Meta):
        model = TextAppSetting
        fields = DefaultAppSettingSerializer.Meta.fields + ("value",)
        update_url_name = "app_settings:update-text"


class ImageAppSettingSerializer(DefaultAppSettingSerializer):
    value = serializers.ImageField(
        max_length=None,
        use_url=True,
        allow_null=True,
        required=False,
    )

    class Meta(DefaultAppSettingSerializer.Meta):
        model = ImageAppSetting
        fields = DefaultAppSettingSerializer.Meta.fields + ("value",)
        update_url_name = "app_settings:update-image"


class EnumAppSettingSerializer(DefaultAppSettingSerializer):
    value = serializers.CharField(
        max_length=255,
        allow_null=True,
        required=False,
    )

    class Meta(DefaultAppSettingSerializer.Meta):
        model = EnumAppSetting
        fields = DefaultAppSettingSerializer.Meta.fields + ("value", "options")
        update_url_name = "app_settings:update-enum"

    def get_options(self, obj):
        return json.loads(obj.options)


class AppSettingCollectionSerializer(serializers.ModelSerializer):
    app_settings = serializers.SerializerMethodField()

    class Meta:
        model = AppSettingCollection
        fields = (
            "id",
            "municipality",
            "app_settings",
        )
        extra_kwargs = {
            "municipality": {"required": False, "allow_null": True},
            "app_settings": {"required": False, "allow_null": True},
        }

    def get_app_settings(self, obj):
        app_settings = []
        app_settings.extend(
            BooleanAppSettingSerializer(
                obj.boolean_app_settings.all(), context=self.context, many=True
            ).data
        )
        app_settings.extend(
            IntegerAppSettingSerializer(
                obj.integer_app_settings.all(), context=self.context, many=True
            ).data
        )
        app_settings.extend(
            FloatAppSettingSerializer(
                obj.float_app_settings.all(), context=self.context, many=True
            ).data
        )
        app_settings.extend(
            ImageAppSettingSerializer(
                obj.image_app_settings.all(), context=self.context, many=True
            ).data
        )
        app_settings.extend(
            EnumAppSettingSerializer(
                obj.enum_app_settings.all(), context=self.context, many=True
            ).data
        )
        app_settings.extend(
            TextAppSettingSerializer(
                obj.text_app_settings.all(), context=self.context, many=True
            ).data
        )
        return app_settings
