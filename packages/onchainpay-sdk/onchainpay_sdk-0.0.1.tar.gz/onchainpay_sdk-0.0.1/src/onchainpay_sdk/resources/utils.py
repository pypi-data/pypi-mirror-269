import hashlib
import hmac

import requests


def create_signature(private_key, message) -> str:
    return hmac.new(
        bytes(private_key, "latin-1"),
        msg=bytes(message, "latin-1"),
        digestmod=hashlib.sha256,
    ).hexdigest()


def check_required_field(field: any, field_name: any) -> None:
    if not field:
        raise ValueError(f"{field_name} is required")


def format_response_error(response: requests.Response) -> dict:
    return {
        "success": False,
        "error": {
            "code": response.status_code,
            "message": response.text,
        }
    }
