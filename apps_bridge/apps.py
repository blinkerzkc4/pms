from django.apps import AppConfig


class AppsBridgeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps_bridge"

    def ready(self):
        import apps_bridge.signals
