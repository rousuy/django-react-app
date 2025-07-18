from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    """
    Custom API exception that supports dynamic field-based messages
    and formatted error messages with translation support.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail: str | dict[str, Promise] | Promise = _("Invalid input.")
    default_code: str = "api_exception_error"


# ======================== Child Exceptions ===============================
class ValidationError(CustomAPIException):
    """Validation error exception."""

    default_code = "validation_error"


class NotFoundError(CustomAPIException):
    """Resource not found exception."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("Resource not found.")
    default_code = "not_found"


class PermissionDeniedError(CustomAPIException):
    """Permission denied exception."""

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("You do not have permission to perform this action.")
    default_code = "permission_denied"


class ConflictError(CustomAPIException):
    """Resource conflict exception."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Resource conflict.")
    default_code = "resource_conflict"


class UnauthorizedError(CustomAPIException):
    """Unauthorized access exception."""

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Authentication credentials were not provided or are invalid.")
    default_code = "unauthorized"


class ServerError(CustomAPIException):
    """Internal server error exception."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Internal server error.")
    default_code = "server_error"
