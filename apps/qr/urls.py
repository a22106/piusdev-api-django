from django.conf import settings
from django.urls import path
from .views import (
    QrUrlView,
    QrEmailView,
    QrTextView,
    QrPhoneNumberView,
    QrVcardView,
    QrWifiView,
    QrSmsView,
    QrGeoView,
    QrEventView,
    QrMeCardView,
    QrWhatsAppView,
    QrBitcoinView,
)



app_name = "qr"


urlpatterns = [
    # API v1
    path("v1/url", QrUrlView.as_view(), name="qr_url_v1"),
    path("v1/email", QrEmailView.as_view(), name="qr_email_v1"),
    path("v1/text", QrTextView.as_view(), name="qr_text_v1"),
    path("v1/phonenumber", QrPhoneNumberView.as_view(), name="qr_phone_number_v1"),
    path("v1/vcard", QrVcardView.as_view(), name="qr_vcard_v1"),
    path("v1/wifi", QrWifiView.as_view(), name="qr_wifi_v1"),
    path("v1/sms", QrSmsView.as_view(), name="qr_sms_v1"),
    path("v1/geo", QrGeoView.as_view(), name="qr_geo_v1"),
    path("v1/event", QrEventView.as_view(), name="qr_event_v1"),
    path("v1/mecard", QrMeCardView.as_view(), name="qr_mecard_v1"),
    path("v1/whatsapp", QrWhatsAppView.as_view(), name="qr_whatsapp_v1"),
    path("v1/bitcoin", QrBitcoinView.as_view(), name="qr_bitcoin_v1"),
]

