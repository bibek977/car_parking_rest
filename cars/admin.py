from django.contrib import admin
from cars.models import *

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['id']

class AreaModelAdmin(admin.ModelAdmin):
    list_display = ['id']

class ParkModelAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(Car,CarModelAdmin)
admin.site.register(AreaName,AreaModelAdmin)
admin.site.register(ParkingDetails,ParkModelAdmin)