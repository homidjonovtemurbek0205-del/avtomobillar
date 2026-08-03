# from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.exceptions import NotFound

from core.models import Avtomobil, IshlabChiqaruvchi
from core.serializers import AvtomobilSerializer, AvtomobilListSerializer, AvtomobilCreateSerializer, IshlabChiqaruvchiSmallSerializer

# Create your views here.
class AvtomobilListCreateView(APIView):
    def get(self, request):
        avtomobillar = Avtomobil.objects.all()
        serializer = AvtomobilListSerializer(avtomobillar, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AvtomobilCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class AvtomobilDetailView(APIView):
    def get(self, request, id):
        try:
            avtomobil = Avtomobil.objects.get(id=id)
        except Avtomobil.DoesNotExist:
            NotFound("Avtomobil topilmadi")
        serializer = AvtomobilSerializer(avtomobil)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            avtomobil = Avtomobil.objects.get(id=id)
        except Avtomobil.DoesNotExist:
            NotFound("Avtomobil topilmadi")
        serializer = AvtomobilSerializer(isinstance=avtomobil, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.save())

    def delete(self, request, id):
        try:
            avtomobil = Avtomobil.objects.get(id=id)
        except Avtomobil.DoesNotExist:
            NotFound("Avtomobil topilmadi")
        avtomobil.delete()
        return Response(status=204)


class IshlabChiqaruvchiListCreateView(APIView):
    def get(self, request):
        ishlab_chiqaruvchilar = IshlabChiqaruvchi.objects.all()
        serializer = IshlabChiqaruvchiSmallSerializer(ishlab_chiqaruvchilar, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IshlabChiqaruvchiSmallSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from core.models import Avtomobil
from core.serializers import (
    AvtomobilSerializer, 
    AvtomobilListSerializer, 
    AvtomobilCreateDetailSerializer
)


class CustomCarPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20


class AvtomobilListAPIView(generics.ListAPIView):
    serializer_class = AvtomobilListSerializer
    pagination_class = CustomCarPagination

    def get_queryset(self):
        queryset = Avtomobil.objects.all()
        marka = self.request.query_params.get('marka')
        min_narx = self.request.query_params.get('min_narx')
        max_narx = self.request.query_params.get('max_narx')
        ishlab_chiqarilgan_yili = self.request.query_params.get('ishlab_chiqarilgan_yili')

        if marka:
            queryset = queryset.filter(markasi__iexact=marka)
        if min_narx:
            queryset = queryset.filter(narxi__gte=min_narx)
        if max_narx:
            queryset = queryset.filter(narxi__lte=max_narx)
        if ishlab_chiqarilgan_yili:
            queryset = queryset.filter(ishlab_chiqarilgan_yili=ishlab_chiqarilgan_yili)

        return queryset


class AvtomobilCreateAPIView(generics.CreateAPIView):
    queryset = Avtomobil.objects.all()
    serializer_class = AvtomobilCreateDetailSerializer

    # 24-topshiriq: perform_create
    def perform_create(self, serializer):
        serializer.save(yaratuvchi='Sanjarbek')


class AvtomobilDetailUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Avtomobil.objects.all()
    
    lookup_field = 'kod'
    lookup_url_kwarg = 'car_code'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AvtomobilCreateDetailSerializer
        return AvtomobilSerializer

    def perform_update(self, serializer):
        serializer.save(oxirgi_tahrirlagan='Akmal')