from django.contrib import admin
from cars.models import AreaName, Car, ParkingDetails
from cars.resource import CarModelResource
from import_export.admin import ImportExportModelAdmin

# class CarModelAdmin(admin.ModelAdmin):
#     list_display = ["liscence"]


class AreaModelAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ParkModelAdmin(admin.ModelAdmin):
    list_display = ["car", "area"]


# admin.site.register(Car, CarModelAdmin)
admin.site.register(AreaName, AreaModelAdmin)
admin.site.register(ParkingDetails, ParkModelAdmin)

@admin.register(Car)
class CarResourceAdmin(ImportExportModelAdmin):
    resource_class=CarModelResource