from typing import Any

from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from src.identity import serializers


class JWTSetCookieMixin:
    def set_cookie(self, response: Response, cookie_name: str, cookie_value: str, max_age: int) -> None:
        response.set_cookie(
            key=cookie_name,
            value=cookie_value,
            max_age=max_age,
            httponly=True,
            samesite="None",
            secure=True,
        )

    def finalize_response(
        self,
        request: Request,
        response: Response,
        *args: str,
        **kwargs: dict[str, Any],
    ) -> Response:
        tokens: dict[str, dict[str, Any]] = {
            "refresh": {
                "name": settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"],
                "lifetime": settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            },
            "access": {
                "name": settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"],
                "lifetime": settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            },
        }

        for token_type, token_settings in tokens.items():
            token_value = response.data.get(token_type)
            if token_value:
                self.set_cookie(
                    response,
                    token_settings["name"],
                    token_value,
                    token_settings["lifetime"],
                )

        return super().finalize_response(request, response, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
