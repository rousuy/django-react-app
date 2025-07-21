from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from src.users.models import User
from src.users.serializers import user_serializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()

    def get_serializer_class(self) -> type:
        serializers_map = {
            "create": user_serializer.UserCreateSerializer,
            "change_password": user_serializer.PasswordChangeSerializer,
            "change_email": user_serializer.EmailChangeSerializer,
        }
        return serializers_map.get(self.action, user_serializer.UserListSerializer)

    def _handle_action(
        self,
        request: Request,
        status_code: int = status.HTTP_204_NO_CONTENT,
    ) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status_code)

    @action(detail=True, methods=["post"], url_path="change-password")
    def change_password(self, request: Request, pk: int) -> Response:
        return self._handle_action(request)

    @action(detail=True, methods=["post"], url_path="change-email")
    def change_email(self, request: Request, pk: int) -> Response:
        return self._handle_action(request)
