from typing import ClassVar

from rest_framework import serializers

from src.users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields: ClassVar[list[str]] = ["id", "email", "password"]
        extra_kwargs: ClassVar[dict[str, dict[str, bool]]] = {"password": {"write_only": True}}

    def create(self, validated_data: dict[str, str]) -> User:
        return self.Meta.model.objects.create_user(**validated_data)  # type: ignore[attr-defined]
