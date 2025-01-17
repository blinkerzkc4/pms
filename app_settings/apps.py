from django.apps import AppConfig


class AppSettingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_settings"

    def ready(self):
        import app_settings.signals
