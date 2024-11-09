import pytest

from core.supabase import supabase




@pytest.mark.django_db
def test_fetch_data():
    response = supabase.table("auth_user").select("*").execute()
    print(response)
    assert isinstance(response.data, list) and len(response.data) > 0


@pytest.mark.django_db
def test_signup_user():
    response = supabase.auth.sign_up(
        {"email": "email@example.com", "password": "password"}
    )
    print(response)
    # email or phone must be provided
    # assert response["status"] == 201
    # assert response["data"]["email"] == "email@example.com"


@pytest.mark.django_db
def test_retrieve_a_user():
    response = supabase.auth.get_user()
    print(response)
