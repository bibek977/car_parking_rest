from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("signup",SignupModelViewSet,basename="signup")
router.register("login",LoginModelViewSet,basename="login")

urlpatterns = [
    path('',include(router.urls)),
]
