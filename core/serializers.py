from rest_framework import serializers

from core.models import Avtomobil


class AvtomobilSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    modeli = serializers.CharField(min_length=2, max_length=50)
    markasi = serializers.CharField(max_length=30)
    narxi = serializers.DecimalField(
        max_digits=20, decimal_places=2, min_value=1000, max_value=1000000
    )
    ishlab_chiqarilgan_yili = serializers.IntegerField(min_value=1990, max_value=2026)
    yurgan_masofasi = serializers.IntegerField(min_value=0, max_value=1000000)
    yoqilgi_turi = serializers.CharField(max_length=20)
    izohi = serializers.CharField(write_only=True, required=False, allow_blank=True)
    yaratilgan_vaqti = serializers.DateTimeField(read_only=True)

    def validate_modeli(self, modeli: str):
        sozlar = ["test", "semo", "sample"]
        for soz in sozlar:
            if modeli.lower().startswith(soz):
                raise serializers.ValidationError(
                    "Avtomobil modeli Test, Demo yoki Sample bilan boshlanishi mumkin emas."
                )
        return modeli

    def validate_markasi(self, markasi: str):
        markalar = ["chevrolet", "kia", "hyundai", "toyota", "bmw"]
        if markasi not in markalar:
            raise serializers.ValidationError(f"Faqat {markalar} bolishi kerak.")
        return markasi

    def validate_narxi(self, narxi):
        if str(narxi).split(".")[0].endswith("999"):
            raise serializers.ValidationError("Narxi 999 bilan tugamasligi kerak.")
        return narxi

    def validate(self, data: dict):
        ishlab_chiqarilgan_yili = data.get("ishlab_chiqarilgan_yili")
        yurgan_masofasi = data.get("yurgan_masofasi")
        narxi = data.get("narxi")
        markasi = data.get("markasi")

        if (
            ishlab_chiqarilgan_yili
            and yurgan_masofasi
            and ishlab_chiqarilgan_yili >= 2024
            and yurgan_masofasi > 50_000
        ):
            raise serializers.ValidationError(
                "Ishlab chiqarilgan yili 2024 yoki undan keyin bo'lsa "
                "yurgan masofasi 50 000 km dan oshmasligi kerak."
            )

        if (
            narxi
            and ishlab_chiqarilgan_yili
            and narxi > 100_000
            and ishlab_chiqarilgan_yili < 2005
        ):
            raise serializers.ValidationError(
                "Narxi 100 000 dan yuqori bo'lsa "
                "avtomobil 2005-yildan eski bo'lishi mumkin emas."
            )

        if markasi and narxi and markasi.lower() == "bmw" and narxi < 30_000:
            raise serializers.ValidationError(
                "Markasi BMW bo'lsa narxi kamida 30 000 bo'lishi kerak"
            )
        return data

    def create(self, validated_data):
        return Avtomobil.objects.create(**validated_data)

    def update(self, instance, validated_data: dict):
        instance.modeli = validated_data.get("modeli", instance.modeli)
        instance.markasi = validated_data.get("markasi", instance.markasi)
        instance.narxi = validated_data.get("narxi", instance.narxi)
        instance.ishlab_chiqarilgan_yili = validated_data.get(
            "ishlab_chiqarilgan_yili", instance.ishlab_chiqarilgan_yili
        )
        instance.yurgan_masofasi = validated_data.get(
            "yurgan_masofasi", instance.yurgan_masofasi
        )
        instance.yoqilgi_turi = validated_data.get(
            "yoqilgi_turi", instance.yoqilgi_turi
        )
        instance.izohi = validated_data.get("izohi", instance.izohi)

        instance.save()
        return instance