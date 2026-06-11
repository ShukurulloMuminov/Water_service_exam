from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Suv, Mijoz, Haydovchi, Buyurtma, Admin


@admin.register(Suv)
class SuvAdmin(TranslationAdmin):
    pass


@admin.register(Mijoz)
class MijozAdmin(TranslationAdmin):
    pass


@admin.register(Haydovchi)
class HaydovchiAdmin(TranslationAdmin):
    pass


@admin.register(Buyurtma)
class BuyurtmaAdmin(admin.ModelAdmin):
    pass


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    pass