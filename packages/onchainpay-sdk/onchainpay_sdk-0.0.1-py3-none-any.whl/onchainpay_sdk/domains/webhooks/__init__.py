from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class Webhooks:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method allows you to get the original body of the webhook.
    
    :param required str webhook_id: Webhook identifier
    :return: dict
    :raise ValueError: if webhook_id is not provided
    
    :example:
    >>> sdk.webhooks.get_webhook_by_id("webhook_id")
    """

    def get_webhook_by_id(self, webhook_id: str):
        check_required_field(webhook_id, "webhook_id")

        payload = {
            "webhookId": webhook_id,
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/webhooks/get",
            payload=payload
        )

    """
    The method allows you to get full information about the webhook.
    
    :param required str webhook_id: Webhook ID
    :param required list fields: Get only necessary fields in response from provided filter
    :return: dict
    :raise ValueError: if webhook_id is not provided
    
    :example:
    >>> sdk.webhooks.get_webhook_by_id_extended("webhook_id", ["field1", "field2"])
    """

    def get_webhook_by_id_extended(self, webhook_id: str, fields: list):
        check_required_field(webhook_id, "webhook_id")

        payload = {
            "webhookId": webhook_id,
            "fields": fields
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/webhooks/get-verbose",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.Webhooks>"
