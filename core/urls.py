from django.urls import path
from core import views
from . import views

urlpatterns = [
    path("api/avtomobillar", views.AvotmobillarListCreateView.as_view(), name='avtomobil-list-create'),
    path("api/avtomobillar/<int:id>", views.AvtomobilDetailView.as_view(), name='avtomobil-detail'),
]