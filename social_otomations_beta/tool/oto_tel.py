import json

import requests
import time
from datetime import datetime, timezone

BASE_URL = "https://www.textverified.com"
CACHE = {}  # Cache mechanism

class TextVerifiedAPI:
    def __init__(self, api_key, email):
        self.api_key = api_key
        self.email = email
        self.bearer_token = None  # Store bearer token in the instance

    def generate_bearer_token(self):
        """Generates a Bearer token and manages it with cache."""
        def is_bearer_token_expired():
            """Checks if the token has expired."""
            token_cache = CACHE.get("token")
            if not token_cache:
                return True

            expiration_str = token_cache.get("expiresAt")
            if expiration_str:
                expiration = datetime.fromisoformat(expiration_str)
                if datetime.now(timezone.utc) >= expiration:
                    return True
            return False

        def get_token_from_cache():
            """Returns the token from cache."""
            token_cache = CACHE.get("token")
            return token_cache.get("token") if token_cache else None

        # Return cached token if it hasn't expired
        if not is_bearer_token_expired():
            self.bearer_token = get_token_from_cache()
            return self.bearer_token

        # Otherwise, request a new token
        headers = {
            "X-API-KEY": self.api_key,
            "X-API-USERNAME": self.email
        }

        response = requests.post(f"{BASE_URL}/api/pub/v2/auth", headers=headers)
        response.raise_for_status()

        data = response.json()
        CACHE["token"] = data  # Save the token to cache
        self.bearer_token = data.get("token")
        return self.bearer_token

    def get_headers(self):
        """Returns the headers with the Bearer token."""
        if not self.bearer_token:
            raise Exception("Bearer token not generated.")
        return {"Authorization": f"Bearer {self.bearer_token}"}

    def get_account_details(self):
        """Retrieves account details."""
        headers = self.get_headers()
        response = requests.get(f"{BASE_URL}/api/pub/v2/account/me", headers=headers)
        response.raise_for_status()
        return response.json()

    def get_service_list(self):
        """Retrieves the list of services."""
        headers = self.get_headers()
        params = {
            "numberType": "mobile",  # mobile, voip, landline
            "reservationType": "verification"  # renewable, verification, etc.
        }
        response = requests.get(f"{BASE_URL}/api/pub/v2/services", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def create_verification(self):
        """Creates a verification process."""
        headers = self.get_headers()
        json_data = {
            "serviceName": "gmail",
            "capability": "sms",  # sms, voice, etc.
        }
        response = requests.post(f"{BASE_URL}/api/pub/v2/verifications", headers=headers, json=json_data)
        response.raise_for_status()
        return response.json()

    def get_verification_details(self, href):
        """Retrieves the details of a specific verification."""
        headers = self.get_headers()
        response = requests.get(href, headers=headers)
        response.raise_for_status()
        return response.json()

    def poll_for_verification(self, href, poll_interval_seconds=10):
        """Polls for verification result at specific intervals, failing after 10 attempts if verification is not complete."""
        max_attempts = 10
        attempts = 0

        while attempts < max_attempts:
            verification_details = self.get_verification_details(href)
            verification_state = verification_details.get("state")

            if verification_state == "verificationCompleted":
                print("\nVerification completed")
                break
            elif verification_state == "verificationPending":
                print("\nPending verification")
                attempts += 1
                time.sleep(poll_interval_seconds)

        if attempts == max_attempts:
            print("Verification failed")
            return True

    def cancel_verification(self, verification_id):
        """Cancels a verification process."""
        url = f"{BASE_URL}/api/pub/v2/verifications/{verification_id}/cancel"
        headers = self.get_headers()
        response = requests.post(url, headers=headers)
        return response.status_code == 200

    def reactivate_verification(self, verification_id):
        """Reactivates a verification process."""
        url = f"{BASE_URL}/api/pub/v2/verifications/{verification_id}/reactivate"
        headers = self.get_headers()
        response = requests.post(url, headers=headers)
        if response.status_code == 201:
            return response.headers.get('Location')
        return None

    def get_sms_details(self, phone_number=None, reservation_id=None, reservation_type="verification"):
        """Retrieves the list of SMS messages for a given phone number or reservation."""
        headers = self.get_headers()
        params = {}
        if phone_number:
            params["to"] = phone_number
        if reservation_id:
            params["reservationId"] = reservation_id
        if reservation_type:
            params["reservationType"] = reservation_type

        response = requests.get(f"{BASE_URL}/api/pub/v2/sms", headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("data", [])  # Returns the list of SMS messages

