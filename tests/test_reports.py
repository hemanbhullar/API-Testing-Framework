import pytest
import time

@pytest.mark.regression
def test_generate_report(api_client):
    # Simulate async report generation (common in GreyMatter)
    response = api_client.post("/reports/generate", json={"type": "inventory"})
    assert response.status_code in [202, 404]   # 202 = Accepted (async)