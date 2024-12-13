from rest_framework.permissions import IsAuthenticated


class SettingBelongsToMunicipality(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            super().has_object_permission(request, view, obj)
            and obj.setting_collection.municipality
            == request.user.assigned_municipality
        )
