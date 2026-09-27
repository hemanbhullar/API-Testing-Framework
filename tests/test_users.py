import pytest
import json


@pytest.mark.smoke
def test_get_single_user(api_client):
    """Basic GET request test"""
    print("token", api_client.token)
    response = api_client.get("/users/2")

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == 2
    assert "email" in data["data"]

with open("../data/test_data/users_data.json") as f:
    sample_user_data = json.load(f)


@pytest.mark.smoke
@pytest.mark.parametrize("users_payload", sample_user_data)
def test_create_user(api_client, users_payload):
    """POST request with payload"""
    response = api_client.post("/users", json=users_payload)

    assert response.status_code == 201
    assert response.json()["name"] == users_payload["name"]


@pytest.mark.regression
def test_update_user(api_client, sample_user_data):
    """PUT request"""
    response = api_client.put("/users/2", json=sample_user_data)

    assert response.status_code == 200
    assert response.json()["job"] == sample_user_data["job"]