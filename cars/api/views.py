from io import BytesIO, StringIO

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils import timezone
from import_export.formats.base_formats import CSV, XLSX
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from cars.models import AreaName, Car, ParkingDetails
from cars.resource import CarModelResource
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

    @action(detail=False, methods=["get"])
    def export_data(self, request):
        user = request.user
        queryset = Car.objects.filter(owner=user)

        format_type = request.query_params.get("format_type", "csv")
        car_resource = CarModelResource()
        dataset = car_resource.export(queryset)

        if format_type == "xlsx":
            format_class = XLSX
            content_type = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            file_extension = "xlsx"
        else:
            format_class = CSV
            content_type = "text/csv"
            file_extension = "csv"

        response = HttpResponse(
            format_class().export_data(dataset), content_type=content_type
        )
        response[
            "Content-Disposition"
        ] = f'attachment; filename="cars.{file_extension}"'
        return response

    @action(detail=False, methods=["post"])
    def import_data(self, request):
        file = request.FILES["file"]
        format_type = request.data.get("format_type", "csv")

        if format_type == "xlsx":
            file_io = BytesIO(file.read())
            format_class = XLSX
        else:
            file_content = file.read().decode("utf-8")
            file_io = StringIO(file_content)
            format_class = CSV

        format_instance = format_class()
        dataset = format_instance.create_dataset(file_io)
        car_resource = CarModelResource()
        result = car_resource.import_data(dataset, dery_run=True)

        if not result.has_errors():
            car_resource.import_data(dataset, dry_run=False)
            return Response({"status": "imported"})
        else:
            return Response({"status": "error", "errors": result.invalid_rows})


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
