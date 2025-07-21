from typing import TypeVar

from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from src.users.exceptions import InvalidEmailError, RequiredFieldError

UserT = TypeVar("UserT", bound="User")  # type: ignore[name-defined] # noqa F821


class UserManager(BaseUserManager[UserT]):
    """
    Custom user manager with email validation and proper exceptions.
    """

    use_in_migrations = True

    def create_user(self, email: str, password: str | None = None, **extra_fields: object) -> UserT:
        """
        Create and return a new user with the given email and password.
        """
        if not email:
            user_model = apps.get_model("users", "User")
            field_name = "email"
            label = user_model._meta.get_field(field_name).verbose_name  # Noqa
            raise RequiredFieldError(field=field_name, label=label)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError as err:
            raise InvalidEmailError from err

        email = self.normalize_email(email)
        user: UserT = self.model(email=email, **extra_fields)  # type: ignore[arg-type]
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str, **extra_fields: object) -> UserT:
        """
        Create and return a new superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email: str) -> UserT:  # type: ignore
        """
        Get user by email (natural key for authentication).
        """
        return self.get(email__iexact=email)
