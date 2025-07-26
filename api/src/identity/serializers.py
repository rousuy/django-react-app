from typing import Any, TypeVar

from django.contrib.auth import get_user_model, user_logged_in
from django.http import HttpRequest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

User = get_user_model()

UserT = TypeVar("UserT", bound=User)  # type: ignore[name-defined]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        data = super().validate(attrs)

        request: HttpRequest | None = self.context.get("request")
        if request:
            user_logged_in.send(
                sender=self.user.__class__,
                request=request,
                user=self.user,
            )
        return data

    @classmethod
    def get_token(cls, user: UserT) -> Token:
        return super().get_token(user)

    @classmethod
    def add_custom_claims(cls, user: UserT, token: Token) -> None:
        token["email"] = user.email
