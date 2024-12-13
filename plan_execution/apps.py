from django.apps import AppConfig


class PlanExecutionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plan_execution"

    def ready(self):
        import plan_execution.signals
