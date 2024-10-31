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
