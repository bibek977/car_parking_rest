from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from cars.models import AreaName, Car, ParkingDetails
from users.custom_permissions import (  # noqa
    BossPermissions,
    EmployeePermissions,
    IsOwner,
    IsOwnerPark,
    ViewerPermissions,
)

from .serializers import AreaSerializer, CarSerializer, ParkSerializer

User = get_user_model()


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    authentication_classes = [JWTAuthentication]
    # authentication_classes = [BasicAuthentication]
    # pagination_class=CustomPagination

    filter_backends = [OrderingFilter]
    filterset_fields = ["brand", "liscence"]
    ordering_fields = ["brand", "liscence"]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.owner == "viewer":
            return Car.objects.filter(owner=user)
        elif user.owner in ["employee", "boss"]:
            return Car.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ["create"]:
            self.permission_classes = [
                IsAuthenticated,
                ViewerPermissions | EmployeePermissions | BossPermissions,
            ]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [
                IsAuthenticated,
                IsOwner | EmployeePermissions | BossPermissions,
            ]
        return [permissions() for permissions in self.permission_classes]


class AreaViewSet(viewsets.ModelViewSet):
    queryset = AreaName.objects.all()
    serializer_class = AreaSerializer

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [
                IsAuthenticated,
                ViewerPermissions | EmployeePermissions | BossPermissions,
            ]
        elif self.action in ["create"]:
            self.permission_classes = [
                IsAuthenticated,
                EmployeePermissions | BossPermissions,
            ]
        elif self.action in ["update", "destroy"]:
            self.permission_classes = [IsAuthenticated, BossPermissions]
        return [permissions() for permissions in self.permission_classes]


class ParkViewSet(viewsets.ModelViewSet):
    queryset = ParkingDetails.objects.all()
    serializer_class = ParkSerializer

    # authentication_classes = [BasicAuthentication]
    authentication_classes = [JWTAuthentication]

    def update(self, request, pk=None):
        try:
            park = ParkingDetails.objects.get(id=pk)
        except ParkingDetails.DoesNotExist:
            return Response({"error": "Parking detail not found"}, status=404)
        park.status = False
        park.checked_out = timezone.now()
        park.save()
        car = Car.objects.get(liscence=park.car)
        car.status = False
        area = AreaName.objects.get(name=park.area)
        area.status = False
        area.save()

        return Response({"data": f"{id} is parked out"})

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [
                IsAuthenticated,
                BossPermissions | EmployeePermissions | IsOwnerPark,
            ]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [
                IsAuthenticated,
                EmployeePermissions | BossPermissions,
            ]
        else:
            self.permission_classes = [
                IsAuthenticated,
                BossPermissions | EmployeePermissions,
            ]

        return [permissions() for permissions in self.permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.owner == "viewer":
            car = Car.objects.filter(owner=user)
            return ParkingDetails.objects.filter(car__in=car)
        elif user.owner in ["employee", "boss"]:
            return ParkingDetails.objects.all()
