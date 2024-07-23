from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginModelViewSet, SignupModelViewSet

router = DefaultRouter()

router.register("signup", SignupModelViewSet, basename="signup")
router.register("login", LoginModelViewSet, basename="login")

urlpatterns = [
    path("", include(router.urls)),
]
