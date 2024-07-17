from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import LoginModelViewSet

router = DefaultRouter()

router.register("login",LoginModelViewSet,basename="login")

urlpatterns = [
    path('',include(router.urls))
]
