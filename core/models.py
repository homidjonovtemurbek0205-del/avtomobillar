from django.db import models


class IshlabChiqaruvchi(models.Model):
    nomi = models.CharField(max_length=100)
    davlati = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nomi


class Avtomobil(models.Model):
    ishlab_chiqaruvchi = models.ForeignKey(IshlabChiqaruvchi, on_delete=models.SET_NULL, null=True, related_name='avtomobillar')

    modeli = models.CharField(max_length=100)
    markasi = models.CharField(max_length=100)
    narxi = models.DecimalField(max_digits=10, decimal_places=2)
    ishlab_chiqarilgan_yili = models.IntegerField()
    yurgan_masofasi = models.IntegerField()
    yoqilgi_turi = models.CharField(max_length=100)
    izohi = models.TextField(blank=True)
    yaratilgan_vaqti = models.DateTimeField(auto_now_add = True)
    yaratuvchi = models.CharField(max_length=100, null=True, blank=True)
    oxirgi_tahrirlagan = models.CharField(max_length=100, null=True, blank=True)
    kod = models.SlugField(unique=True, null=True, blank=True)