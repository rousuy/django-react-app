from typing import Any, ClassVar

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.users.exceptions import PasswordMistmatchError
from src.users.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields: ClassVar[list[str]] = ["id", "email"]
        read_only_fields: ClassVar[list[str]] = ["id"]
        abstract = True  # symbolic marker only; DRF doesn't support abstract serializers natively

    def __init_subclass__(cls: type[Any], **kwargs: Any) -> None:  # Noqa
        super().__init_subclass__(**kwargs)
        # Prevent direct instantiation of the base serializer.
        if cls.__name__ == "BaseUserSerializer":
            error = "Cannot instantiate BaseUserSerializer directly. Use a subclass instead."
            raise TypeError(error)


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields: ClassVar[list[str]] = [*BaseUserSerializer.Meta.fields, "password"]
        extra_kwargs: ClassVar[dict[str, dict[str, bool]]] = {"password": {"write_only": True}}

    def validate_password(self, arg: str) -> str:
        try:
            validate_password(arg)
        except DjangoValidationError as error:
            raise ValidationError(error.messages) from error
        return arg

    def create(self, validated_data: dict[str, str]) -> User:
        return self.Meta.model.objects.create_user(**validated_data)  # type: ignore[attr-defined]


class UserListSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields: ClassVar[list[str]] = [*BaseUserSerializer.Meta.fields, "is_active"]


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        user: User = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise PasswordMistmatchError
        try:
            validate_password(attrs["new_password"], user=user)
        except ValidationError as error:
            raise ValidationError({"new_password": error.messages}) from error  # type: ignore[defined-attr]

        return attrs

    def save(self, **kwargs: dict[str, Any]) -> User:
        user: User = self.context["request"].user
        user.set_password(self.validated_data["new_password"])  # type: ignore
        user.save(update_fields=["password"])
        return user
