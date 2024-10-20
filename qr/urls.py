from django.urls import path
from .views import IndexView, QrImageView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("qr_image/", QrImageView.as_view(), name="qr_image"),
    path("v1/qr_image/", QrImageView.as_view(), name="qr_image_v1"),
]
