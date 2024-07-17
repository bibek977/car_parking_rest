from rest_framework import viewsets
from cars.models import *
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from .custom_page import *
from cars.utils import today_date
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class=CarSerializer

    # permission_classes=[IsAuthenticated]
    pagination_class=CustomPagination

    filter_backends=[OrderingFilter]
    filterset_fields=['brand','liscence']

class AreaViewSet(viewsets.ModelViewSet):
    queryset=AreaName.objects.all()
    serializer_class=AreaSerializer

    permission_classes=[IsAuthenticated]

class ParkViewSet(viewsets.ModelViewSet):
    queryset=ParkingDetails.objects.all()
    serializer_class=ParkSerializer

    permission_classes=[IsAuthenticated]
    
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
