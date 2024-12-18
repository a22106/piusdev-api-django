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
    path("v1/qr/url/", QrUrlView.as_view(), name="qr_url_v1"),
    path("v1/qr/email/", QrEmailView.as_view(), name="qr_email_v1"),
    path("v1/qr/text/", QrTextView.as_view(), name="qr_text_v1"),
    path("v1/qr/phonenumber/", QrPhoneNumberView.as_view(), name="qr_phone_number_v1"),
    path("v1/qr/vcard/", QrVcardView.as_view(), name="qr_vcard_v1"),
    path("v1/qr/wifi/", QrWifiView.as_view(), name="qr_wifi_v1"),
    path("v1/qr/sms/", QrSmsView.as_view(), name="qr_sms_v1"),
    path("v1/qr/geo/", QrGeoView.as_view(), name="qr_geo_v1"),
    path("v1/qr/event/", QrEventView.as_view(), name="qr_event_v1"),
    path("v1/qr/mecard/", QrMeCardView.as_view(), name="qr_mecard_v1"),
    path("v1/qr/whatsapp/", QrWhatsAppView.as_view(), name="qr_whatsapp_v1"),
    path("v1/qr/bitcoin/", QrBitcoinView.as_view(), name="qr_bitcoin_v1"),

    # 웹 인터페이스 엔드포인트
    path("url/", QrUrlView.as_view(), name="url"),
    path("email/", QrEmailView.as_view(), name="email"),
    path("text/", QrTextView.as_view(), name="text"),
    path("phone/", QrPhoneNumberView.as_view(), name="phone"),
    path("vcard/", QrVcardView.as_view(), name="vcard"),
    path("wifi/", QrWifiView.as_view(), name="wifi"),
    path("sms/", QrSmsView.as_view(), name="sms"),
    path("geo/", QrGeoView.as_view(), name="geo"),
    path("event/", QrEventView.as_view(), name="event"),
    path("mecard/", QrMeCardView.as_view(), name="mecard"),
    path("whatsapp/", QrWhatsAppView.as_view(), name="whatsapp"),
    path("bitcoin/", QrBitcoinView.as_view(), name="bitcoin"),
]

