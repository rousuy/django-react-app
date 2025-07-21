from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _

from src.shared.exceptions import CustomAPIException


class RequiredFieldError(CustomAPIException):
    """
    Raised when a required field is missing.
    """

    default_code = "required_field"

    def __init__(self, field: str, label: str | Promise) -> None:
        self.default_detail = {field: _(f"The field {label} is required.")}
        super().__init__()


class InvalidEmailError(CustomAPIException):
    """
    Raised when the provided email address is invalid.
    """

    default_code = "invalid_email"
    default_detail = _("The email address is invalid.")


class PasswordMistmatchError(CustomAPIException):
    """
    Raised when password mismatch.
    """

    default_code = "password_mismatch"
    default_detail = _("The passwords do not match.")


class EmailMistmatchError(CustomAPIException):
    """
    Raised when email mismatch.
    """

    default_code = "email_mismatch"
    default_detail = _("Current email does not match.")



class EmailValidationError(CustomAPIException):
    """
    Raised when email mismatch.
    """

    default_code = "email_validation_error"
    default_detail = _("New email must be different from the current email.")
