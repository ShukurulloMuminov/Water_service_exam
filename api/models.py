from django.db import models
from django.contrib.auth.models import AbstractUser



class Admin(AbstractUser):
    yosh = models.PositiveIntegerField(default=18)
    ish_vaqti = models.CharField(max_length=50, default="09:00 - 18:00")

    def __str__(self):
        return self.username



class Suv(models.Model):
    brend = models.CharField(max_length=100)
    narx = models.DecimalField(max_digits=10, decimal_places=2)
    litr = models.FloatField()
    batafsil = models.TextField(blank=True)

    def __str__(self):
        return f"{self.brend} - {self.litr}L"


class Mijoz(models.Model):
    ism = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    manzil = models.TextField()
    qarz = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.ism



class Haydovchi(models.Model):
    SMENA_CHOICES = [
        ('ertalab', 'Ertalab (06:00-14:00)'),
        ('kunduz', 'Kunduz (14:00-22:00)'),
        ('kechasi', 'Kechasi (22:00-06:00)'),
    ]
    ism = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    smena = models.CharField(max_length=20, choices=SMENA_CHOICES)

    def __str__(self):
        return self.ism



class Buyurtma(models.Model):
    suv = models.ForeignKey(Suv, on_delete=models.CASCADE)
    mijoz = models.ForeignKey(Mijoz, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    haydovchi = models.ForeignKey(Haydovchi, on_delete=models.SET_NULL, null=True)
    sana = models.DateTimeField(auto_now_add=True)
    miqdor = models.PositiveIntegerField()
    umumiy_narx = models.DecimalField(max_digits=12, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        # Umumiy narxni avtomatik hisoblash
        self.umumiy_narx = self.suv.narx * self.miqdor
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.mijoz.ism} - {self.suv.brend} x{self.miqdor}"
