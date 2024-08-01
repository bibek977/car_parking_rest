from modeltranslation.translator import register, TranslationOptions
from cars.models import Car, AreaName

@register(Car)
class CarTranslationOptions(TranslationOptions):
    fields = ('brand', 'color', 'liscence')  

@register(AreaName)
class AreaNameTranslationOptions(TranslationOptions):
    fields = ('name',)