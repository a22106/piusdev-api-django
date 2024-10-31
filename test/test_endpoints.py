import unittest
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class QrApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_qr_url_view(self):
        query_params = {"url": "http://example.com"}
        url = reverse("qr:qr_url_v1")
        response = self.client.get(url, query_params)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR],
        )
        self.assertIn("image/png", response["Content-Type"])

    def test_qr_email_view(self):
        query_params = {
            "email": "bk22106@piusdev.com",
            "subject": "Test Subject",
            "body": "Test Body",
        }
        url = reverse("qr:qr_email_v1")
        response = self.client.get(url, query_params)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR],
        )
        self.assertIn("image/png", response["Content-Type"])

    def test_qr_text_view(self):
        query_params = {"text": "Hello, World!"}
        url = reverse("qr:qr_text_v1")
        response = self.client.get(url, query_params)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR],
        )
        self.assertIn("image/png", response["Content-Type"])

    def test_qr_phone_number_view(self):
        query_params = {"phone": "+1234567890"}
        url = reverse("qr:qr_phone_number_v1")
        response = self.client.get(url, query_params)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR],
        )
        self.assertIn("image/png", response["Content-Type"])

    def test_qr_wifi_view(self):
        query_params = {
            "ssid": "TestSSID",
            "password": "TestPassword",
            "encryption": "WPA",
        }
        url = reverse("qr:qr_wifi_v1")
        response = self.client.get(url, query_params)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR],
        )
        self.assertIn("image/png", response["Content-Type"])

    def test_qr_vcard_view(self):
        query_params = {
            "first_name": "John",
            "last_name": "Doe",
            "vcard_email": "john@example.com",
            "vcard_mobile": "1234567890",
            "organization": "Test Corp",
            "title": "Developer",
            "address": "123 Test St",
            "label": "Work",
            "vcard_url": "http://example.com",
            "note": "Test note",
        }
        url = reverse("qr:qr_vcard_v1")
        response = self.client.get(url, query_params)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR],
        )
        self.assertIn("image/png", response["Content-Type"])


if __name__ == "__main__":
    unittest.main()
