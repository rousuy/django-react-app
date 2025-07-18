"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from config.views import healthcheck

# Constants for base URL paths
DJANGO_URL = "django"
API_URL = "api"

# OpenAPI / Swagger documentation routes
open_api_patterns = [
    path(
        "",
        SpectacularAPIView.as_view(),
        name="openapi-schema",
    ),  # OpenAPI JSON schema endpoint
    path(
        "swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="openapi-schema"),
        name="swagger-ui",
    ),  # Interactive Swagger UI
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="openapi-schema"),
        name="redoc",
    ),  # Redoc API documentation UI
]

urlpatterns = [
    # Django Admin interface (internal administrative access)
    path(f"{DJANGO_URL}/admin/", admin.site.urls),
    # API routes including OpenAPI schema and docs
    path(f"{API_URL}/schema/", include(open_api_patterns), name="api-schema"),
    # Health check endpoint for uptime monitoring
    path(f"{API_URL}/health/", healthcheck, name="healthcheck"),
    # Main API endpoints for user-related operations
    path(f"{API_URL}/", include("src.users.urls"), name="users"),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug-only routes
if settings.DEBUG == "False":
    urlpatterns += [path(f"{DJANGO_URL}/silk/", include("silk.urls"), name="silk")]  # Django profiling ui
