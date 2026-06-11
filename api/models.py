from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Admin(AbstractUser):
    yosh = models.PositiveIntegerField(default=18, verbose_name=_('Yosh'))
    ish_vaqti = models.CharField(max_length=50, default="09:00 - 18:00", verbose_name=_('Ish vaqti'))

    class Meta:
        verbose_name = _('Admin')
        verbose_name_plural = _('Adminlar')

    def __str__(self):
        return self.username


class Suv(models.Model):
    brend = models.CharField(max_length=100, verbose_name=_('Brend'))
    narx = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Narx'))
    litr = models.FloatField(verbose_name=_('Litr'))
    batafsil = models.TextField(blank=True, verbose_name=_('Batafsil'))

    class Meta:
        verbose_name = _('Suv')
        verbose_name_plural = _('Suvlar')

    def __str__(self):
        return f"{self.brend} - {self.litr}L"


class Mijoz(models.Model):
    ism = models.CharField(max_length=100, verbose_name=_('Ism'))
    tel = models.CharField(max_length=20, verbose_name=_('Telefon'))
    manzil = models.TextField(verbose_name=_('Manzil'))
    qarz = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_('Qarz'))

    class Meta:
        verbose_name = _('Mijoz')
        verbose_name_plural = _('Mijozlar')

    def __str__(self):
        return self.ism


class Haydovchi(models.Model):
    SMENA_CHOICES = [
        ('ertalab', _('Ertalab (06:00-14:00)')),
        ('kunduz', _('Kunduz (14:00-22:00)')),
        ('kechasi', _('Kechasi (22:00-06:00)')),
    ]
    ism = models.CharField(max_length=100, verbose_name=_('Ism'))
    tel = models.CharField(max_length=20, verbose_name=_('Telefon'))
    smena = models.CharField(max_length=20, choices=SMENA_CHOICES, verbose_name=_('Smena'))

    class Meta:
        verbose_name = _('Haydovchi')
        verbose_name_plural = _('Haydovchilar')

    def __str__(self):
        return self.ism


class Buyurtma(models.Model):
    suv = models.ForeignKey(Suv, on_delete=models.CASCADE, verbose_name=_('Suv'))
    mijoz = models.ForeignKey(Mijoz, on_delete=models.CASCADE, verbose_name=_('Mijoz'))
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, verbose_name=_('Admin'))
    haydovchi = models.ForeignKey(Haydovchi, on_delete=models.SET_NULL, null=True, verbose_name=_('Haydovchi'))
    sana = models.DateTimeField(auto_now_add=True, verbose_name=_('Sana'))
    miqdor = models.PositiveIntegerField(verbose_name=_('Miqdor'))
    umumiy_narx = models.DecimalField(max_digits=12, decimal_places=2, blank=True, verbose_name=_('Umumiy narx'))

    class Meta:
        verbose_name = _('Buyurtma')
        verbose_name_plural = _('Buyurtmalar')

    def save(self, *args, **kwargs):
        self.umumiy_narx = self.suv.narx * self.miqdor
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.mijoz.ism} - {self.suv.brend} x{self.miqdor}"