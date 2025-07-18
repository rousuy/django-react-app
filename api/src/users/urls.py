from rest_framework.routers import DefaultRouter

from src.users.views.user_view import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls
