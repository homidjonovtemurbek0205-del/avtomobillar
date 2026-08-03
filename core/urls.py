from django.urls import path
from core import views

urlpatterns = [
    path("api/avtomobillar", views.AvtomobilListCreateView.as_view(), name="avtomobillar-list"),
    path("api/avtomobillar/<slug:car_code>", views.AvtomobilDetailView.as_view(), name="avtomobil-detail"),
    path("api/ishlab-chiqaruvchi", views.IshlabChiqaruvchiListCreateView.as_view(), name="ishlab_chiqaruvchi-list"),
]