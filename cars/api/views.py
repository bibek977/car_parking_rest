from rest_framework import viewsets
from cars.models import *
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from .custom_page import *
from cars.utils import today_date
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.custom_permissions import *
from django.contrib.auth import get_user_model
User=get_user_model()

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class=CarSerializer

    authentication_classes=[JWTAuthentication]
    # pagination_class=CustomPagination

    filter_backends=[OrderingFilter]
    filterset_fields=['brand','liscence']
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        if user.owner=="viewer":
            return Car.objects.filter(owner=user)
        elif user.owner in ['employee','boss']:
            return Car.objects.all()
        

class AreaViewSet(viewsets.ModelViewSet):
    queryset=AreaName.objects.all()
    serializer_class=AreaSerializer

    authentication_classes=[JWTAuthentication]
        
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[ViewerPermissions | EmployeePermissions | BossPermissions]
        elif self.action in ['create']:
            self.permission_classes=[EmployeePermissions | BossPermissions]
        elif self.action in ['update','destroy']:
            self.permission_classes=[BossPermissions]
        else:
            self.permission_classes=[]
        return [permissions() for permissions in self.permission_classes]

class ParkViewSet(viewsets.ModelViewSet):
    queryset=ParkingDetails.objects.all()
    serializer_class=ParkSerializer

    authentication_classes=[JWTAuthentication]

    def update(self,request,pk=None):
        id=pk
        park=ParkingDetails.objects.get(id=id)
        park.status=False
        # park.checked_out=today_date
        park.save()
        car=Car.objects.get(liscence=park.car)
        car.status=False
        area=AreaName.objects.get(name=park.area)
        area.status=False
        area.save()
        
        return Response({'data':f'{id} is parked out'})

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[ViewerPermissions | BossPermissions | EmployeePermissions]
        if self.action=='update':
            self.permission_classes=[EmployeePermissions | BossPermissions]
        if self.action=="create":
            self.permission_classes=[BossPermissions | EmployeePermissions]

        return [permissions() for permissions in self.permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.owner=="viewer":
            car = Car.objects.filter(owner=user)
            return ParkingDetails.objects.filter(car__in=car)
        elif user.owner in ["employee","boss"]:
            return ParkingDetails.objects.all()