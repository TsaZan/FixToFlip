from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "FixToFlip.accounts"

    def ready(self):
        import FixToFlip.accounts.signals
