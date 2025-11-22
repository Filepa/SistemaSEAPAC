from django.apps import AppConfig


class SeapacConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "seapac"

    def ready(self):
        import seapac.signals
