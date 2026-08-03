from rest_framework import serializers
from core.models import Avtomobil, IshlabChiqaruvchi
from datetime import datetime



class IshlabChiqaruvchiSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = IshlabChiqaruvchi
        fields = ['id', 'nomi', 'email']

class AvtomobilSerializer(serializers.ModelSerializer):
    izohi = serializers.CharField(write_only=True, required=False, allow_blank=True)
    modeli = serializers.CharField(min_length=2, max_length=50, help_text="Avtomobil modelini kiriting (masalan: Cobalt, Gentra)")
    yoshi = serializers.SerializerMethodField()
    ishlab_chiqaruvchi = IshlabChiqaruvchiSmallSerializer(read_only=True)
    ishlab_chiqaruvchi_email = serializers.SlugRelatedField(queryset = IshlabChiqaruvchi.objects.all(), source='ishlab_chiqaruvchi', slug_field = 'email')

    class Meta:
        model = Avtomobil
        fields = ['id', 'modeli', 'markasi', 'narxi', 'ishlab_chiqarilgan_yili', 'yurgan_masofasi', 'yoqilgi_turi', 'izohi', 'yaratilgan_vaqti', 'yoshi', 'ishlab_chiqaruvchi', 'ishlab_chiqaruvchi_email']

        read_only_fields = ['id', 'yaratilgan_vaqti']

    def get_yoshi(self, obj):
        joriy_yil = datetime.now().year
        return joriy_yil - obj.ishlab_chiqarilgan_yili

class AvtomobilListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avtomobil
        fields = ['id', 'modeli']


class AvtomobilCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avtomobil
        exclude = ['id', 'yaratilgan_vaqti']


    def create(self, validated_data):
        validated_data['modeli'] = str(validated_data['modeli']).strip().title()
        if validated_data.get("markasi"):
            validated_data['markasi'] = str(validated_data['markasi']).strip().title()
        return super().create(validated_data)



class AvtomobilCreateDetailSerializer(serializers.ModelSerializer):
    ishlab_chiqaruvchi = IshlabChiqaruvchiSmallSerializer(required=False)
    
    toliq_nomi = serializers.SerializerMethodField()
    premium = serializers.SerializerMethodField()
    eski_avtomobil = serializers.SerializerMethodField()

    class Meta:
        model = Avtomobil
        exclude = ['id', 'yaratilgan_vaqti']

    def get_toliq_nomi(self, obj):
        return f"{obj.markasi} {obj.modeli}"

    def get_premium(self, obj):
        return obj.narxi >= 50000

    def get_eski_avtomobil(self, obj):
        joriy_yil = datetime.now().year
        yoshi = joriy_yil - obj.ishlab_chiqarilgan_yili
        return yoshi > 15

    def create(self, validated_data):
        ishlab_chiqaruvchi_data = validated_data.pop('ishlab_chiqaruvchi', None)
        
        if ishlab_chiqaruvchi_data:
            ishlab_chiqaruvchi_obj, _ = IshlabChiqaruvchi.objects.get_or_create(
                email=ishlab_chiqaruvchi_data.get('email'),
                defaults=ishlab_chiqaruvchi_data
            )
            validated_data['ishlab_chiqaruvchi'] = ishlab_chiqaruvchi_obj

        if validated_data.get('modeli'):
            validated_data['modeli'] = str(validated_data['modeli']).strip().title()
        if validated_data.get('markasi'):
            validated_data['markasi'] = str(validated_data['markasi']).strip().title()

        return super().create(validated_data)