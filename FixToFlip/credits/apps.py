from django.apps import AppConfig


class CreditsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "FixToFlip.credits"

    def ready(self):
        import FixToFlip.credits.signals
