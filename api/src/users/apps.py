from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.users"

    def ready(self) -> None:
        """Import signals when the app is ready."""
        import src.users.utils.signals  # noqa
