import requests
import base64
import time
from config import Config
from services.token_store import get_refresh_token, save_refresh_token


class SchwabClient:
    def __init__(self):
        self.access_token = None
        self.expiry = 0

    def _refresh_access_token(self):
        refresh_token = get_refresh_token()
        if not refresh_token:
            raise Exception("No refresh token stored")

        credentials = f"{Config.SCHWAB_CLIENT_ID}:{Config.SCHWAB_CLIENT_SECRET}"
        encoded = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        response = requests.post(
            Config.SCHWAB_TOKEN_URL,
            headers=headers,
            data=data,
            timeout=10
        )

        if response.status_code != 200:
            raise Exception("Token refresh failed")

        tokens = response.json()

        self.access_token = tokens["access_token"]
        self.expiry = time.time() + tokens["expires_in"]

        # Handle rotating refresh tokens
        if "refresh_token" in tokens:
            save_refresh_token(tokens["refresh_token"])

    def _get_valid_token(self):
        if not self.access_token or time.time() >= self.expiry:
            self._refresh_access_token()
        return self.access_token

    def get_positions(self):
        token = self._get_valid_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(
            "https://api.schwabapi.com/trader/v1/accounts?fields=positions",
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            raise Exception("Failed to fetch positions")

        return response.json()
