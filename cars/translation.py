from modeltranslation.translator import TranslationOptions, register

from cars.models import AreaName, Car


@register(Car)
class CarTranslationOptions(TranslationOptions):
    fields = ("brand", "color", "liscence")


@register(AreaName)
class AreaNameTranslationOptions(TranslationOptions):
    fields = ("name",)
