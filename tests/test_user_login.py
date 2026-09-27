import pytest
import requests
from utils import data_loader

user_data = data_loader.read_json_data("../data/test_data/user_login.json")

@pytest.mark.parametrize(
    "email, password", user_data
)
@pytest.mark.smoke
def test_user_login(email, password):
    print("user_data", user_data)
    payload = {"email": email, "password": password}
    headers = {"Content-Type": "application/json"}
    response = requests.post("https://ultronapi-g-s.sourcerer.tech/users/v1/login", json=payload, headers=headers)
    assert response.status_code == 200
    print(response.text)
    token = response.json()["token"]
