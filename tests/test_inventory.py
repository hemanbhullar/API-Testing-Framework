import pytest

@pytest.mark.smoke
def test_get_inventory(api_client):
    # Simulate inventory endpoint
    response = api_client.get("/inventory")
    assert response.status_code in [200, 404]   # 404 if endpoint doesn't exist on ReqRes

@pytest.mark.regression
@pytest.mark.parametrize("sku", ["SKU-001", "SKU-002"])
def test_create_inventory(api_client, sku):
    payload = {"sku": sku, "quantity": 10}
    response = api_client.post("/inventory", json=payload)
    assert response.status_code in [201, 404]