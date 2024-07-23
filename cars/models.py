import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Car(BaseModel):
    brand = models.CharField(_("car_brand"), max_length=100)
    color = models.CharField(_("color_of_car"), max_length=50)
    liscence = models.CharField(
        _("liscence_number"), max_length=20, unique=True
    )  # noqa
    status = models.BooleanField(_("car_status"), default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("All_Cars")

    def __str__(self):
        return self.liscence


class AreaName(BaseModel):
    name = models.CharField(_("area_name"), max_length=200, unique=True)
    status = models.BooleanField(_("area_status"), default=False)

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Total_Area")

    def __str__(self):
        return self.name


class ParkingDetails(BaseModel):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="liscences"
    )  # noqa
    area = models.ForeignKey(
        AreaName, on_delete=models.CASCADE, related_name="areas"
    )  # noqa
    status = models.BooleanField(_("parking_status"), default=True)
    checked_in = models.DateTimeField(_("date_checked_in"), auto_now_add=True)
    checked_out = models.DateTimeField(
        _("date_checked_out"), blank=True, null=True
    )  # noqa

    class Meta:
        verbose_name = _("Parking")
        verbose_name_plural = _("Parking_Details")

    def __str__(self):
        return f"{str(self.car)} : {str(self.area)}"


@receiver(post_save, sender=ParkingDetails)
def parked_in(sender, instance, created, **kwargs):
    if created:
        area = AreaName.objects.get(id=instance.area.id)
        area.status = True
        area.save()

        car = Car.objects.get(id=instance.car.id)
        car.status = True
        car.save()
