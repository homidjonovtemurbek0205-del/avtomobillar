from django.db import models

class Avtomobil(models.Model):
    modeli = models.CharField(max_length=100)
    markasi = models.CharField(max_length=100)
    narxi = models.DecimalField(max_digits=10, decimal_places=2)
    ishlab_chiqarilgan_yili = models.IntegerField()
    yurgan_masofasi = models.IntegerField()
    yoqilgi_turi = models.CharField(max_length=100)
    izohi = models.TextField(blank=True)
    yaratilgan_vaqti = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return self.modeli