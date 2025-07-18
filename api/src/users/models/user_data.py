from dataclasses import dataclass

from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _


@dataclass(frozen=True)
class _Meta:
    """
    Immutable container for metadata of a model field.

    Attributes:
        name (str): Internal field name used in code and data structures.
        label (str): Human-readable and translatable label for UI display and error messages.
    """

    name: str
    label: str | Promise


class UserData:
    """
    Field metadata definitions for the User model.

    This class centralizes the technical field names and user-friendly labels
    to ensure consistent use throughout validation, serialization, and error handling.
    """

    EMAIL = _Meta(name="email", label=_("Email"))
    PASSWORD = _Meta(name="password", label=_("Password"))


class ProfileData:
    """
    Field metadata definitions for the Profile model.

    This class centralizes the technical field names and user-friendly labels
    specific to the Profile model, used consistently across the codebase.
    """

    FIRST_NAME = _Meta(name="first_name", label=_("First Name"))
    LAST_NAME = _Meta(name="last_name", label=_("Last Name"))
    PHONE_NUMBER = _Meta(name="phone_number", label=_("Phone Number"))
    BIO = _Meta(name="bio", label=_("Biography"))
