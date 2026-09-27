import pytest
import os
from dotenv import load_dotenv
from utils.api_client import ApiClient
load_dotenv()



@pytest.fixture(scope="session")
def api_client():
    """
        Session-scoped fixture → created once for the entire test run.
        This is the professional way: authenticate only once.
        """
    base_url = os.getenv("BASE_URL", "https://reqres.in/api")
    client = ApiClient(base_url)

    client.authenticate(
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET")
    )

    yield client

    # Teardown (runs after all tests finish)
    print("\n[Teardown] Closing API session...")
    client.session.close()

@pytest.fixture
def sample_user_data():
    """Reusable test data fixture"""
    return {
        "name": "morpheus",
        "job": "leader"
    }

# Example of a marker (we'll use this in pytest.ini later)
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: quick sanity tests")
    config.addinivalue_line("markers", "regression: full regression suite")
