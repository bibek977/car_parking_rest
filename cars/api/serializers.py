from django.contrib.auth import get_user_model
from django.utils.translation import get_language
from rest_framework import serializers

from cars.models import AreaName, Car, ParkingDetails

User = get_user_model()


User = get_user_model()


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "brand", "color", "liscence", "status", "owner"]
        read_only_fields = ["owner"]

    def get_translated_field(self, obj, field_name):
        """
        Returns the translated value of a field based on the current language.
        """
        language = get_language()
        field_name_with_lang = f"{field_name}_{language}"
        return getattr(obj, field_name_with_lang, getattr(obj, field_name))

    # def get_owner_email(self,obj):
    #     return obj.owner.email

    def to_representation(self, instance):
        """
        Customize the representation of the instance to include translated fields.
        """
        ret = super().to_representation(instance)
        ret["brand"] = self.get_translated_field(instance, "brand")
        ret["color"] = self.get_translated_field(instance, "color")
        ret["owner"] = instance.owner.name
        return ret


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaName
        fields = ["id", "name", "status"]

    def get_translated_field(self, obj, field_name):
        """
        Returns the translated value of a field based on the current language.
        """
        language = get_language()
        field_name_with_lang = f"{field_name}_{language}"
        return getattr(obj, field_name_with_lang, getattr(obj, field_name))

    def to_representation(self, instance):
        """
        Customize the representation of the instance to include translated fields.
        """
        ret = super().to_representation(instance)
        ret["name"] = self.get_translated_field(instance, "name")
        return ret


class ParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingDetails
        fields = ["id", "car", "area", "status", "checked_in", "checked_out"]

    def validate(self, data):
        car = data.get("car")
        if Car.objects.get(liscence=car).status is True:
            raise serializers.ValidationError(f"Car : {car} is still parked in")  # noqa
        area = data.get("area")
        if AreaName.objects.get(name=area).status is True:
            raise serializers.ValidationError(
                f"Area : {area} is alreay occupied"
            )  # noqa
        return data

    def get_checked_in_formatted(self, obj):
        if obj.checked_in:
            return obj.checked_in.strftime("%d-%m-%Y : %H:%M")
        return None

    def get_checked_out_formatted(self, obj):
        if obj.checked_out:
            return obj.checked_out.strftime("%d-%m-%Y : %H:%M")
        return None

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["car"] = instance.car.liscence
        ret["area"] = instance.area.name
        ret["checked_in"] = self.get_checked_in_formatted(instance)
        ret["checked_out"] = self.get_checked_out_formatted(instance)

        return ret
