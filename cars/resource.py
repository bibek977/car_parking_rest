from import_export.resources import ModelResource

from cars.models import Car


class CarModelResource(ModelResource):
    def before_import_row(self, row, **kwargs):
        print(f"Before importing row : {row}")

    def after_import_row(self, row, row_result, **kwargs):
        print(f"After importing row: {row}")

    def before_export(self, queryset, *args, **kwargs):
        print("Car dataset ready to export")

    def after_export(self, queryset, data, *args, **kwargs):
        print("Car dataset exported")

    class Meta:
        model = Car
        list_display = ["liscence", "brand", "color"]
