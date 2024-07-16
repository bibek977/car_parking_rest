from django.urls import path,include
from rest_framework.routers import DefaultRouter
from cars.api.views import *

router = DefaultRouter()

router.register('cars',CarViewSet,basename='cars')

urlpatterns = [
    path('',include(router.urls))
]
