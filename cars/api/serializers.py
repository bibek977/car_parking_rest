from django.contrib.auth import get_user_model
from rest_framework import serializers

from cars.models import *

User = get_user_model()


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "brand", "color", "liscence", "status", "owner"]
        read_only_fields = ["owner"]

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            validated_data["owner"] = request.user
        return super().create(validated_data)


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaName
        fields = ["id", "name", "status"]


class ParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingDetails
        fields = ["id", "car", "area", "status", "checked_in", "checked_out"]

    def validate(self, data):
        car = data.get("car")
        if Car.objects.get(liscence=car).status == True:
            raise serializers.ValidationError(
                f"Car : {car} is still parked in")
        area = data.get("area")
        if AreaName.objects.get(name=area).status == True:
            raise serializers.ValidationError(
                f"Area : {area} is alreay occupied")
        return data
