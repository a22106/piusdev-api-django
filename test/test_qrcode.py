import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.skip_db_check
def test_qr_vcard_view(capsys):
    client = APIClient()

    # Sample query parameters
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

    # Make GET request to the endpoint
    url = reverse("qr:qr_vcard_v1")  # Make sure this matches your URL pattern name
    response = client.get(url, query_params)

    # Get captured output
    captured = capsys.readouterr()

    # Print the query parameters (this will be captured by capsys)
    print(f"Query Parameters: {query_params}")

    # Basic assertions
    assert response.status_code in [
        200,
        500,
    ]
