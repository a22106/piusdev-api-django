from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("qr_image/", views.qr_image, name="qr_image"),
]
