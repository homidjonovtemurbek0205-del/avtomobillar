from rest_framework import serializers 
from core.models import Avtomobil


class AvtomobilSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    modeli = serializers.CharField(max_length=100)
    markasi = serializers.CharField(max_length=100) 
    narxi = serializers.DecimalField(max_digits=10, decimal_places=2)
    ishlab_chiqarilgan_yili = serializers.IntegerField()
    yurgan_masofasi = serializers.IntegerField()
    yoqilgi_turi = serializers.CharField()
    izohi = serializers.CharField()
    yaratilgan_vaqti = serializers.DateTimeField(read_only=True) 



    def validate_narxi(self, narxi:int):
        if str(narxi).endswith('999'):
            raise serializers.ValidationError("Narxi '999' bilan tugagan qiymatlar qabul qilinmaydi")
        return narxi

    def validate(self, data):
        ishlab_chiqarilgan_yili = data['ishlab_chiqarilgan_yili']
        yurgan_masofasi = data['yurgan_masofasi']
        if ishlab_chiqarilgan_yili>2024:
            if yurgan_masofasi>50000:
                raise serializers.ValidationError("Yili 2024dan kichik bolgan mashinalarning yurgan masofasi 50.000kmdan oshmasligi kerak ")
        return data

    def validate(self, data):
        narxi = data["narxi"]
        ishlab_chiqarilgan_yili = data['ishlab_chiqarilgan_yili']
        if narxi >100000:
            if ishlab_chiqarilgan_yili>2015:
                raise serializers.ValidationError("Narxi 100.000dan balanda bo'lgan mashinalarni ishlab chiqarilgan yili 2015dan yangi bo'lishi kerak")
        return data

    def validate(self, data):
        modeli = data["modeli"]
        narxi = data['narxi']
        if modeli == 'BMW':
            if narxi > 30000:
                raise serializers.ValidationError("Modeli 'BMW' bo'lgan mashinalarning narxi kamida 30.000 bo'lishi kerak ")
        return data

    def create(self, validated_data):
        return Avtomobil.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.modeli = validated_data.get('modeli', instance.modeli)
        instance.markasi = validated_data.get('markasi', instance.markasi)
        instance.narxi = validated_data.get("narxi", instance.narxi)
        instance.ishlab_chiqarilgan_yili = validated_data.get('ishlab_chiqarilgan_yili', instance.ishlab_chiqarilgan_yili)
        instance.yurgan_masofasi = validated_data.get('yurgan_masofasi', instance.yurgan_masofasi)
        instance.yoqilgi_turi = validated_data.get("yoqilgi_turi", instance.yoqilgi_turi)
        instance.izohi = validated_data.get('izohi', instance.izohi)


        instance.save()
        return instance