from django.apps import apps
from django.contrib import admin

# Register your models here.
app = apps.get_app_config("project_report")


class TemplateFieldMappingAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "name_eng", "field_type")
    list_filter = ("field_type",)
    search_fields = ("code", "name", "name_eng", "field_type")
    ordering = ("id",)


admin_page_mapping = {"templatefieldmapping": TemplateFieldMappingAdmin}

for model_name, model in app.models.items():
    try:
        if model_name in admin_page_mapping.keys():
            admin.site.register(model, admin_page_mapping[model_name])
        else:
            admin.site.register(model)
    except Exception as e:
        print(f"Exception: {e}")
        pass
