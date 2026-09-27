import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()


class ApiClient:
    def __init__(self, base_url=None):
        # Use BASE_URL from .env if not passed directly
        self.base_url = base_url or os.getenv("BASE_URL", "https://reqres.in/api")

        # Create a session (reuses connections → faster & handles cookies)
        self.session = requests.Session()

        # Professional retry logic (handles temporary server issues)
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.mount("http://", HTTPAdapter(max_retries=retries))

        self.token = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def _request(self, method, endpoint, **kwargs):
        """Core method that handles all HTTP requests"""
        url = f"{self.base_url}{endpoint}"

        # Add auth header if token exists
        headers = kwargs.pop("headers", {})
        if self.token:
            headers.setdefault("Authorization", f"Bearer {self.token}")
        headers.setdefault("Content-Type", "application/json")
        headers.setdefault("Accept", "application/json")

        try:
            response = self.session.request(
                method, url, headers=headers, timeout=30, **kwargs
            )
            response.raise_for_status()  # Raise error for 4xx/5xx
            self.logger.info(f"{method} {endpoint} → {response.status_code}")
            return response
        except Exception as e:
            self.logger.error(f"Request failed: {method} {endpoint} → {e}")
            raise

        # Convenience methods (cleaner test code)

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)

    def authenticate(self, username=None, password=None, client_id=None, client_secret=None):
        """
        OAuth2 Password Grant
        """
        if not username or not password:
            self.token = None
            return

        #token endpoint
        token_url = "/api-gateway/auth-service/platform-auth/oauth/token"

        payload = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "read write"
        }

        # Basic auth with client credentials (common pattern)
        auth = (client_id or "your-client-id", client_secret or "your-client-secret")

        try:
            resp = self.session.post(
                f"{self.base_url}{token_url}",
                data=payload,
                auth=auth,
                timeout=30
            )
            resp.raise_for_status()
            token_data = resp.json()
            self.token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
            self.logger.info("OAuth authentication successful")
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            raise
