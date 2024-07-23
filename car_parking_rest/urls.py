from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cars.api.urls")),
    path("users/", include("users.api.urls")),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),  # noqa
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # noqa
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # noqa
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
