from modeltranslation.translator import register, TranslationOptions
from .models import Suv, Mijoz, Haydovchi, Buyurtma


@register(Suv)
class SuvTranslationOptions(TranslationOptions):
    fields = ('brend', 'batafsil')


@register(Mijoz)
class MijozTranslationOptions(TranslationOptions):
    fields = ('ism', 'manzil')


@register(Haydovchi)
class HaydovchiTranslationOptions(TranslationOptions):
    fields = ('ism',)


@register(Buyurtma)
class BuyurtmaTranslationOptions(TranslationOptions):
    fields = ()

