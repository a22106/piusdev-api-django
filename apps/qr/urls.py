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
    # v1 prefix 제거
    path("url/", QrUrlView.as_view(), name="qr_url_v1"),
    path("email/", QrEmailView.as_view(), name="qr_email_v1"),
    path("text/", QrTextView.as_view(), name="qr_text_v1"),
    path("phonenumber/", QrPhoneNumberView.as_view(), name="qr_phone_number_v1"),
    path("vcard/", QrVcardView.as_view(), name="qr_vcard_v1"),
    path("wifi/", QrWifiView.as_view(), name="qr_wifi_v1"),
    path("sms/", QrSmsView.as_view(), name="qr_sms_v1"),
    path("geo/", QrGeoView.as_view(), name="qr_geo_v1"),
    path("event/", QrEventView.as_view(), name="qr_event_v1"),
    path("mecard/", QrMeCardView.as_view(), name="qr_mecard_v1"),
    path("whatsapp/", QrWhatsAppView.as_view(), name="qr_whatsapp_v1"),
    path("bitcoin/", QrBitcoinView.as_view(), name="qr_bitcoin_v1"),
]

