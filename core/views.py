from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.exceptions import NotFound
from core.models import Avtomobil
from core.serializers import AvtomobilSerializer

class AvotmobillarListCreateView(APIView):
    def get(self, request):
        avtomobillar = Avtomobil.objects.all()
        serializer = AvtomobilSerializer(avtomobillar, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AvtomobilSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AvtomobilDetailView(APIView):
    def get(self, request, id):
        try:
            avtomobil = Avtomobil.objects.get(id=id)
        except Avtomobil.DoesNotExist:
            raise NotFound("Avtomobil topilmadi")

        serializer = AvtomobilSerializer(avtomobil)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            avtomobil = Avtomobil.objects.get(id=id)
        except Avtomobil.DoesNotExist:
            raise NotFound("Avtomobil Topilmadi")

        s = AvtomobilSerializer(instance =avtomobil, data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)