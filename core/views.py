# from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.exceptions import NotFound

from core.models import Avtomobil
from core.serializers import AvtomobilSerializer


# Create your views here.
class AvtomobilListCreateView(APIView):
    def get(self, request):
        avtomobillar = Avtomobil.objects.all()
        serializer = AvtomobilSerializer(avtomobillar, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AvtomobilSerializer(data=request.data)
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