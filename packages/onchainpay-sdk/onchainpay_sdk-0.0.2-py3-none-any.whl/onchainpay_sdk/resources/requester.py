import json
from random import random

import requests
from onchainpay_sdk.resources.constants import REQUEST_TIMEOUT_RESPONSE
from onchainpay_sdk.resources.utils import create_signature, format_response_error


class APIRequestor:
    def __init__(
            self,
            public_key: str,
            private_key: str,
            url: str,
            payload: dict = None
    ):
        self.url = url

        self.headers = {}
        self.payload = payload or {}

        self.set_nonce()
        self.set_auth_headers(public_key, private_key)

    def set_nonce(self):
        self.payload.update({"nonce": round(random() * 1000000000)})

    def set_auth_headers(self, public_key: str, secret: str):
        self.headers.update(
            {
                "x-api-public-key": public_key,
                "x-api-signature": create_signature(secret, json.dumps(self.payload)),
            }
        )

    def post(self):
        try:
            response = requests.post(
                self.url,
                json=self.payload,
                headers=self.headers,
            )
        except requests.exceptions.Timeout:
            return REQUEST_TIMEOUT_RESPONSE

        if response.status_code >= 400:
            try:
                return response.json()
            except json.JSONDecodeError:
                return format_response_error(response)

        return response
