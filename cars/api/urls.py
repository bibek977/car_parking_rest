from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cars.api.views import *

router = DefaultRouter()

router.register("cars", CarViewSet, basename="cars")
router.register("area", AreaViewSet, basename="area")
router.register("park", ParkViewSet, basename="park")

urlpatterns = [path("", include(router.urls))]
