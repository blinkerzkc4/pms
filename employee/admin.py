from django.apps import apps
from django.contrib import admin

app = apps.get_app_config("employee")
# Register your models here.


for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except Exception as e:
        print(f"Exception: {e}")
        pass
