from django.urls import path, reverse
from .views import IndexView, QrImageView, HelloWorldView, HelloDjangoView, QrApiView

app_name = "qr"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("qr_image/", QrImageView.as_view(), name="qr_image"),
    path("v1/qr_image/", QrApiView.as_view(), name="qr_image_v1"),
    path("v1/hello_world/", HelloWorldView.as_view(), name="hello_world_v1"),
    path("v1/hello_django/", HelloDjangoView.as_view(), name="hello_django_v1"),
]
