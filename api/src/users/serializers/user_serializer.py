from typing import Any, ClassVar

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.users import exceptions
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
    password = serializers.CharField(
        write_only=True,
        label=_("Password"),
        help_text=_("Enter a strong password"),
        style={"input_type": "password"},
    )

    class Meta(BaseUserSerializer.Meta):
        fields: ClassVar[list[str]] = [*BaseUserSerializer.Meta.fields, "password"]

    def validate_password(self, value: str) -> str:
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise ValidationError(detail=exc.messages) from exc
        return value

    def create(self, validated_data: dict[str, str]) -> User:
        return self.Meta.model.objects.create_user(**validated_data)  # type: ignore[attr-defined]


class UserListSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields: ClassVar[list[str]] = [*BaseUserSerializer.Meta.fields, "is_active"]
        read_only_fields: ClassVar[list[str]] = [*BaseUserSerializer.Meta.read_only_fields, "email"]


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        label=_("Old password"),
        style={"input_type": "password"},
    )
    new_password = serializers.CharField(
        write_only=True,
        label=_("New password"),
        style={"input_type": "password"},
    )

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        user: User = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise exceptions.PasswordMistmatchError

        try:
            validate_password(attrs["new_password"], user=user)
        except DjangoValidationError as exc:
            raise ValidationError({"new_password": exc.messages}) from exc

        return attrs

    def save(self, **kwargs: dict[str, Any]) -> User:
        user: User = self.context["request"].user
        user.set_password(self.validated_data["new_password"])  # type: ignore
        user.save(update_fields=["password"])
        return user


class EmailChangeSerializer(serializers.Serializer):
    old_email = serializers.EmailField(
        write_only=True,
        label=_("Current email"),
    )
    new_email = serializers.EmailField(
        write_only=True,
        label=_("New email"),
    )

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        user: User = self.context["request"].user

        if user.email != attrs["old_email"]:
            raise exceptions.EmailMistmatchError

        if user.email == attrs["new_email"]:
            raise exceptions.EmailValidationError

        try:
            validate_email(attrs["new_email"])
        except DjangoValidationError as exc:
            raise ValidationError({"new_email": exc.messages}) from exc

        return attrs

    def save(self, **kwargs: dict[str, Any]) -> User:
        user: User = self.context["request"].user
        user.email = self.validated_data["new_email"]  # type: ignore
        user.save(update_fields=["email"])
        return user
