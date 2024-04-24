from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class Webhooks:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method allows you to get the original body of the webhook.
    
    :param required str webhookId: Webhook identifier
    :return: dict
    :raise ValueError: if webhookId is not provided
    
    :example:
    >>> sdk.webhooks.get_webhook_by_id("8d7db145-80cc-4c43-9cfb-9cde10f8ef40")
    """

    def get_webhook_by_id(self, webhookId: str):
        check_required_field(webhookId, "webhookId")

        payload = {
            "webhookId": webhookId,
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/webhooks/get",
            payload=payload
        )

    """
    The method allows you to get full information about the webhook.
    
    :param required str webhookId: Webhook ID
    :param required list fields: Get only necessary fields in response from provided filter
    :return: dict
    :raise ValueError: if webhookId is not provided
    
    :example:
    >>> sdk.webhooks.get_webhook_by_id_extended(
            "8d7db145-80cc-4c43-9cfb-9cde10f8ef40", 
            ["id", "event"]
        )
    """

    def get_webhook_by_id_extended(self, webhookId: str, fields: list):
        check_required_field(webhookId, "webhookId")

        payload = {
            "webhookId": webhookId,
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
