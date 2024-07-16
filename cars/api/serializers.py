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