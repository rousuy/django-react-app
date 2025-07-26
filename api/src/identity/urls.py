from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from src.identity.views import CustomTokenObtainPairView

# Constants URL paths
TOKEN_URL = "token"


urlpatterns = [
    # JWT Token endpoints
    path(f"{TOKEN_URL}/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(f"{TOKEN_URL}/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
