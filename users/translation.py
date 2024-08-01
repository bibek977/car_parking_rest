from modeltranslation.translator import TranslationOptions, register

from users.models import CustomUser


@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    fields = ("name",)
