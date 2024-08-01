from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from cars.models import AreaName, Car, ParkingDetails
from cars.resource import CarModelResource

from modeltranslation.admin import TranslationAdmin


class AreaModelAdmin(TranslationAdmin):
    list_display = ('name', 'status')
    search_fields = ('name',)  
    list_filter = ('status',) 

admin.site.register(AreaName, AreaModelAdmin)


class ParkModelAdmin(admin.ModelAdmin):
    list_display = ["car", "area"]

admin.site.register(ParkingDetails, ParkModelAdmin)


@admin.register(Car)
class CarResourceAdmin(ImportExportModelAdmin, TranslationAdmin):
    resource_class = CarModelResource
    list_display = ('brand', 'color', 'liscence', 'status', 'owner')
    search_fields = ('brand', 'color', 'liscence')
    list_filter = ('status', 'owner')