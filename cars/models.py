from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save

class BaseModel(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Car(BaseModel):
    brand = models.CharField(_("car_brand"),max_length=100)
    color = models.CharField(_("color_of_car"),max_length=50)
    liscence = models.CharField(_("liscence_number"),max_length=20,unique=True)
    status = models.BooleanField(_("car_status"),default=False)

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("All_Cars")

    def __str__(self):
        return self.liscence

class AreaName(BaseModel):
    name=models.CharField(_("area_name"),max_length=200,unique=True)
    status=models.BooleanField(_("area_status"),default=False)

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Total_Area")

    def __str__(self):
        return self.name

class ParkingDetails(BaseModel):
    car=models.ForeignKey(Car,on_delete=models.CASCADE)
    area=models.ForeignKey(AreaName,on_delete=models.CASCADE)
    status=models.BooleanField(_("parking_status"),default=True)
    checked_in=models.DateTimeField(_("date_checked_in"),auto_now=True)
    checked_out=models.DateTimeField(_("date_checked_out"),blank=True,null=True)

    class Meta:
        verbose_name = _("Parking")
        verbose_name_plural = _("Parking_Details")

    def __str__(self):
        return f"{str(self.car)} : {str(self.area)}"
    
@receiver(post_save, sender=ParkingDetails)
def parked_in(sender,instance,created,**kwargs):
    if created:
        area=AreaName.objects.get(name=instance.area)
        area.status=True
        area.save()

        car=Car.objects.get(liscence=instance.car)
        car.status=True
        car.save()