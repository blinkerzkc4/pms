from django.contrib import admin

from .models import ActivityType, Norm, NormActivity, NormComponent, NormExtraCost


@admin.register(NormComponent, NormExtraCost, NormActivity, ActivityType)
class UserAddAdmin(admin.ModelAdmin):
    readonly_fields = ("created_by",)

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.created_by = request.user
            super().save_model(request, obj, form, change)

        else:
            super().save_model(request, obj, form, change)


@admin.register(Norm)
class NormAdmin(UserAddAdmin):
    list_filter = ["project"]
