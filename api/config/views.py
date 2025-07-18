from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpRequest, JsonResponse


def healthcheck(request: HttpRequest) -> JsonResponse:
    """
    Returns the health status of the API server and its primary database connection.
    """
    checks: dict[str, str] = {}

    # Check if the default database is reachable
    try:
        connections["default"].cursor()
        checks["database"] = "ok"
    except OperationalError:
        checks["database"] = "unavailable"

    is_healthy = all(status == "ok" for status in checks.values())
    http_status = 200 if is_healthy else 503

    return JsonResponse(
        {"status": "ok" if is_healthy else "error", "checks": checks},
        status=http_status,
    )
