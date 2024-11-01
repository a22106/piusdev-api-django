from django.conf import settings
from django.urls import path, reverse
from .views import (
    IndexView,
    HelloWorldView,
    HelloDjangoView,
    QrUrlView,
    QrEmailView,
    QrTextView,
    QrPhoneNumberView,
    QrVcardView,
    QrWifiView,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "qr"

schema_view = get_schema_view(
    openapi.Info(
        title="QR Code API",
        default_version="v1",
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
    path("api/", schema_view.with_ui("redoc", cache_timeout=0), name="api"),
    # API v1
    path("v1/qr/url/", QrUrlView.as_view(), name="qr_url_v1"),
    path("v1/qr/email/", QrEmailView.as_view(), name="qr_email_v1"),
    path("v1/qr/text/", QrTextView.as_view(), name="qr_text_v1"),
    path("v1/qr/phonenumber/", QrPhoneNumberView.as_view(), name="qr_phone_number_v1"),
    path("v1/qr/vcard/", QrVcardView.as_view(), name="qr_vcard_v1"),
    path("v1/qr/wifi/", QrWifiView.as_view(), name="qr_wifi_v1"),
]

if settings.DEBUG:
    urlpatterns += [
        path("v1/hello_world/", HelloWorldView.as_view(), name="hello_world_v1"),
        path("v1/hello_django/", HelloDjangoView.as_view(), name="hello_django_v1"),
    ]
