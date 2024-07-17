from cars.models import *
from rest_framework import serializers

class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = [
            'id',
            'brand',
            'color',
            'liscence',
            'status'
            ]

class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AreaName
        fields = [
            'id',
            'name',
            'status'
        ]

class ParkSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingDetails
        fields = [
            'id',
            'car',
            'area',
            'status',
            'checked_in',
            'checked_out'
        ]
    def validate(self, data):
        car=data.get('car')
        if Car.objects.get(liscence=car).status==True:
            raise serializers.ValidationError(f'Car : {car} is still parked in')
        area=data.get('area')
        if AreaName.objects.get(name=area).status==True:
            raise serializers.ValidationError(f'Area : {area} is alreay occupied')
        return data
    