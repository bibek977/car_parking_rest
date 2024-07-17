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
        check_car = Car.objects.filter(id=id)
        if check_car:
            car = Car.objects.get(id=id)
            serializer = CarSerializer(car)
            response={
                'data':serializer.data
            }
            return Response(response,status=status.HTTP_200_OK)
        response = {
            'data' : f'{id} not found'
        }
        return Response(response)

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
        return Response(response,status=status.HTTP_201_CREATED)

    def update(self,request,pk=None):
        id=pk
        car=Car.objects.filter(id=id)
        if car:
            car = Car.objects.get(id=id)
            serializer=CarSerializer(car,data=request.data)
            if serializer.is_valid():
                serializer.save()
                response={
                    'data':serializer.data
                }
                return Response(response,status=status.HTTP_200_OK)
            response={
                'data':serializer.errors
            }
            return Response(response,status=status.HTTP_200_OK)
        response={
                'data':f'{id} not matched'
            }
        return Response(response,status=status.HTTP_200_OK)

    def partial_update(self,request,pk=None):
        id=pk
        car=Car.objects.filter(id=id)
        if car:
            car=Car.objects.get(id=id)
            serializer=CarSerializer(car,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                response={
                    'data':serializer.data
                }
                return Response(response,status=status.HTTP_200_OK)
            response={
                'data':serializer.errors
            }
            return Response(response,status=status.HTTP_200_OK)
        response={
            'data':f'{id} not found'
        }
        return Response(response,status=status.HTTP_200_OK)

    def destroy(self,request,pk=None):
        id=pk
        car=Car.objects.filter(id=id)
        if car:
            car=Car.objects.get(id=id)
            car.delete()
            response = {
                'data':f'{id} deleted'
            }
            print(f"{id}")
            return Response(response,status=status.HTTP_200_OK)
        response = {
            'data':f'{id} not found'
        }
        return Response(response,status=status.HTTP_200_OK)
