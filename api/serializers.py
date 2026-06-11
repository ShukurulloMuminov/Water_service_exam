from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Admin, Suv, Mijoz, Haydovchi, Buyurtma


class SuvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suv
        fields = '__all__'

    def validate_litr(self, value):
        if value > 19:
            raise serializers.ValidationError(_("Bunday katta litrlarda suv sotilmaydi"))
        return value


class MijozSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mijoz
        fields = '__all__'


class HaydovchiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Haydovchi
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'username', 'first_name', 'last_name', 'yosh', 'ish_vaqti', 'email']

    def validate_yosh(self, value):
        if value < 19:
            raise serializers.ValidationError(_("Yoshingiz mos kelmaydi"))
        return value


class BuyurtmaSerializer(serializers.ModelSerializer):
    suv_nomi = serializers.CharField(source='suv.brend', read_only=True)
    mijoz_ismi = serializers.CharField(source='mijoz.ism', read_only=True)

    class Meta:
        model = Buyurtma
        fields = '__all__'
        read_only_fields = ['umumiy_narx', 'sana', 'suv_nomi', 'mijoz_ismi']

    def validate(self, data):
        mijoz = data.get('mijoz')
        if mijoz and mijoz.qarz > 500000:
            raise serializers.ValidationError(_("Qarzingiz juda ko'p, buyurtma qilolmaysiz!"))
        return data