import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_qr_url_view(api_client):
    query_params = {"url": "http://example.com"}
    url = reverse("qr:qr_url_v1")
    response = api_client.get(url, query_params)
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    assert "image/png" in response["Content-Type"]


@pytest.mark.django_db
def test_qr_email_view(api_client):
    query_params = {
        "email": "bk22106@piusdev.com",
        "subject": "Test Subject",
        "body": "Test Body",
    }
    url = reverse("qr:qr_email_v1")
    response = api_client.get(url, query_params)
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    assert "image/png" in response["Content-Type"]


@pytest.mark.django_db
def test_qr_text_view(api_client):
    query_params = {"text": "Hello, World!"}
    url = reverse("qr:qr_text_v1")
    response = api_client.get(url, query_params)
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    assert "image/png" in response["Content-Type"]


@pytest.mark.django_db
def test_qr_phone_number_view(api_client):
    query_params = {"phone_number": "01099473728"}
    url = reverse("qr:qr_phone_number_v1")
    response = api_client.get(url, query_params)
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    assert "image/png" in response["Content-Type"]


@pytest.mark.django_db
def test_qr_wifi_view(api_client):
    query_params = {
        "ssid": "TestSSID",
        "password": "TestPassword",
        "encryption": "WPA",
    }
    url = reverse("qr:qr_wifi_v1")
    response = api_client.get(url, query_params)
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    assert "image/png" in response["Content-Type"]


@pytest.mark.django_db
def test_qr_vcard_view(api_client):
    query_params = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "mobile": "1234567890",
        "organization": "Test Corp",
        "title": "Developer",
        "address": "123 Test St",
        "label": "Work",
        "url": "http://example.com",
        "note": "Test note",
    }
    url = reverse("qr:qr_vcard_v1")
    response = api_client.get(url, query_params)
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    assert "image/png" in response["Content-Type"]


@pytest.mark.django_db
def test_qr_sms_view(api_client):
    query_params = {
        "phone_number": "01099473728",
        "message": "Test SMS message",
    }
    url = reverse("qr:qr_sms_v1")
    response = api_client.get(url, query_params)
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    assert "image/png" in response["Content-Type"]


@pytest.mark.django_db
def test_qr_geo_view(api_client):
    query_params = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "query": "San Francisco",
        "zoom": 10,
    }
    url = reverse("qr:qr_geo_v1")
    response = api_client.get(url, query_params)
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    assert "image/png" in response["Content-Type"]


@pytest.mark.django_db
def test_qr_whatsapp_view(api_client):
    query_params = {
        "phone_number": "01099473728",
        "message": "Test WhatsApp message",
    }
    url = reverse("qr:qr_whatsapp_v1")
    response = api_client.get(url, query_params)
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]
    assert "image/png" in response["Content-Type"]
