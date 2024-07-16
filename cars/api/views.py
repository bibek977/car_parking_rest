from rest_framework.response import Response
from rest_framework import viewsets
from cars.api.serializers import *
from cars.models import *
from rest_framework import status

class CarViewSet(viewsets.ViewSet):
    
    def list(self,request):
        car = Car.objects.all()
        serializer = CarSerializer(car,many=True)
        response = {
            'data' : serializer.data,
        }
        return Response(response,status=status.HTTP_200_OK)

    def retrieve(self,request,pk=None):
        id = pk
        if id:
            car = Car.objects.get(id=id)
            serializer = CarSerializer(car)
            response={
                'data':serializer.data
            }
            return Response(response,status=status.HTTP_302_FOUND)
        response = {
            'data' : f'{id} not found'
        }
        return Response(response,status=status.HTTP_404_NOT_FOUND)

    def create(self,request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                'data':f'{serializer.data["id"]} created'
            }
            return Response(response,status=status.HTTP_201_CREATED)
        response={
            'data':serializer.errors
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        id=pk
        car=Car.objects.get(id=id)
        serializer=CarSerializer(car,data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                'data':f'{serializer.data["id"]} is updated'
            }
            return Response(response,status=status.HTTP_205_RESET_CONTENT)
        response={
            'data':f'{serializer.data["id"]} not found'
        }
        return Response(response,status=status.HTTP_304_NOT_MODIFIED)

    def destroy(self,request,pk=None):
        id=pk
        car=Car.objects.get(id=id)
        car.delete()
        response = {
            'data':f'{id} deleted'
        }
        return Response(response,status=status.HTTP_200_OK)
