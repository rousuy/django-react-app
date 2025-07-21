from __future__ import annotations

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.users.models.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using email as the unique identifier.
    first_name, and last_name are removed.
    """

    email = models.EmailField(unique=True, verbose_name=_("Email"))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []  # noqa: RUF012

    objects = UserManager()

    def __str__(self) -> str:
        """
        Return the string representation of the user.
        """
        return self.email
