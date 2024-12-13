from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from app_settings.models import (
    AppSetting,
    AppSettingCollection,
    BooleanAppSetting,
    EnumAppSetting,
    FloatAppSetting,
    ImageAppSetting,
    IntegerAppSetting,
    TextAppSetting,
)
from app_settings.permissions import SettingBelongsToMunicipality
from app_settings.serializers import AppSettingCollectionSerializer
from user.permissions import AdminsOnlyPermission
from utils.report_utils import get_field_value_from_object


class AppSettingUpdateView(APIView):
    permission_classes = [SettingBelongsToMunicipality]
    setting_model: AppSetting = None

    def get_value_from_request(self, request):
        return request.data.get("value")

    def post(self, request, *args, **kwargs):
        app_setting = get_object_or_404(
            self.setting_model, pk=kwargs.get("app_setting_id")
        )
        if app_setting.setting_function == "local_value":
            app_setting.value = self.get_value_from_request(request)
            app_setting.save()
        else:
            new_value = self.get_value_from_request(request)
            in_app_setting_object = app_setting.setting_model_obj
            in_app_model_field = app_setting.in_app_model_field.split(".")
            if len(in_app_model_field) == 1:
                setattr(in_app_setting_object, in_app_model_field[0], new_value)
            else:
                setattr(
                    get_field_value_from_object(
                        in_app_setting_object, in_app_model_field[:-1]
                    ),
                    in_app_model_field[-1],
                    new_value,
                )
            in_app_setting_object.save()
            app_setting.save()
        return Response(status=200)


class BooleanAppSettingUpdateView(AppSettingUpdateView):
    setting_model = BooleanAppSetting

    def get_value_from_request(self, request):
        value = request.data.get("value")
        if isinstance(value, str):
            return value.lower() == "true"
        elif isinstance(value, bool):
            return value
        else:
            return bool(value)


class IntegerAppSettingUpdateView(AppSettingUpdateView):
    setting_model = IntegerAppSetting

    def get_value_from_request(self, request):
        return int(request.data.get("value"))


class FloatAppSettingUpdateView(AppSettingUpdateView):
    setting_model = FloatAppSetting

    def get_value_from_request(self, request):
        return float(request.data.get("value"))


class ImageAppSettingUpdateView(AppSettingUpdateView):
    setting_model = ImageAppSetting


class TextAppSettingUpdateView(AppSettingUpdateView):
    setting_model = TextAppSetting


class EnumAppSettingUpdateView(AppSettingUpdateView):
    setting_model = EnumAppSetting


class AppSettingCollectionView(APIView):
    permission_classes = [AdminsOnlyPermission]

    def get(self, request, *args, **kwargs):
        app_settings_collection = get_object_or_404(
            AppSettingCollection, municipality=request.user.assigned_municipality
        )
        app_setting_collection_serializer = AppSettingCollectionSerializer(
            app_settings_collection, context={"request": request}
        )
        return Response(app_setting_collection_serializer.data)
