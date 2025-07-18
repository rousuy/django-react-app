from rest_framework import mixins, viewsets

from src.users.models import User
from src.users.serializers.user_serializer import UserCreateSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
