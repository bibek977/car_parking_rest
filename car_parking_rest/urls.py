from django.conf.urls.i18n import i18n_patterns, set_language
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),  # noqa
]

urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # noqa
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # noqa
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns += i18n_patterns(
    path("", include("cars.api.urls")),
    path("users/", include("users.api.urls")),
    path("i18n/set_language/", set_language, name="set_language"),
    path("rosetta/", include("rosetta.urls")),
    path("admin/", admin.site.urls),
)
