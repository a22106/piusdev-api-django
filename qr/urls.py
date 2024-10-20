from django.conf import settings
from django.urls import path, reverse
from .views import IndexView, QrImageView, HelloWorldView, HelloDjangoView, QrApiView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "qr"

schema_view = get_schema_view(
    openapi.Info(
        title="QR Code API",
        default_version='v1',
        description="API documentation for QR Code generator",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@qr.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("qr_image/", QrImageView.as_view(), name="qr_image"),
    path("v1/qr_image/", QrApiView.as_view(), name="qr_image_v1"),
    path("api/", schema_view.with_ui("redoc", cache_timeout=0), name="api"),
]

if settings.DEBUG:
    urlpatterns += [
        path("v1/hello_world/", HelloWorldView.as_view(), name="hello_world_v1"),
        path("v1/hello_django/", HelloDjangoView.as_view(), name="hello_django_v1"),
    ]
