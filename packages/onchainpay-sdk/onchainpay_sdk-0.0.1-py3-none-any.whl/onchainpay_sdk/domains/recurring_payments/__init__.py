from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class RecurringPayments:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method creates a temporary link to connect the user. The user must follow the link and 
    give permission to spend coins from his address. After that, you will receive a webhook with 
    the status and payment link ID
    
    :param required str merchant_id: Merchant ID in the system
    :param required str client_id: Client ID in the merchant system
    :param required str client_email: Client's mail in the merchant's system
    :param str client_name: Client name in the merchant system
    :param str return_url: URL to be used as "Return to Store" link
    :param str webhook_url: URL to notify about connecting or denying a client's connection request
    :return: dict
    :raise ValueError: if merchant_id, client_id or client_email is not provided    
    
    :example:
    >>> sdk.recurring_payments.create_payment_link(
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a", 
            "id1234", 
            "maiL@example.com",
        )
    """

    def create_payment_link(
            self,
            merchant_id: str,
            client_id: str,
            client_email: str,
            client_name: str = None,
            return_url: str = None,
            webhook_url: str = None,
    ):
        check_required_field(merchant_id, "merchant_id")
        check_required_field(client_id, "client_id")
        check_required_field(client_email, "client_email")

        payload = {
            "merchantId": merchant_id,
            "clientId": client_id,
            "clientEmail": client_email,
            "clientName": client_name,
            "returnUrl": return_url,
            "webhookUrl": webhook_url
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/create-subscriber-billing-link",
            payload=payload
        )

    """
    The method allows you to get payment link data
    
    :param required str payment_link_id: ID of the payment link in the system
    :param required str merchant_id: Merchant ID in the system
    :return: dict
    :raise ValueError: if payment_link_id or merchant_id is not provided
    
    :example:
    >>> sdk.recurring_payments.get_payment_link(
        "d56bcbe4-586f-4980-b6ca-6e9f557750e8", 
        "672c1e2d-354f-49a1-8a5b-75af87e92f0a"
    )
    """

    def get_payment_link(self, payment_link_id: str, merchant_id: str):
        check_required_field(payment_link_id, "payment_link_id")
        check_required_field(merchant_id, "merchant_id")

        payload = {
            "id": payment_link_id,
            "merchantId": merchant_id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/get-billing-link",
            payload=payload
        )

    """
    The method allows you to get a list of payment links for a specific user
    
    :param required str merchant_id: Merchant ID in the system
    :param str client_id: Client ID in the merchant system
    :param str client_email: Client's mail in the merchant's system
    :return: dict
    :raise ValueError: if merchant_id is not provided
    
    :example:
    >>> sdk.recurring_payments.get_payment_links("672c1e2d-354f-49a1-8a5b-75af87e92f0a")
    """

    def get_payment_links(self, merchant_id: str, client_id: str = None, client_email: str = None):
        check_required_field(merchant_id, "merchant_id")

        payload = {
            "merchantId": merchant_id,
            "clientId": client_id,
            "clientEmail": client_email
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/get-billing-links-by-subscriber",
            payload=payload
        )

    """
    The method allows you to disable the payment link. You will no longer be able to connect 
    subscriptions and make payments using this payment link
    
    :param required str payment_link_id: ID of the payment link in the system
    :param required str merchant_id: Merchant ID in the system
    :return: dict
    :raise ValueError: if payment_link_id or merchant_id is not provided
    
    :example:
    >>> sdk.recurring_payments.disable_payment_link(
            "d56bcbe4-586f-4980-b6ca-6e9f557750e8", 
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a"
        )
    """

    def disable_payment_link(self, payment_link_id: str, merchant_id: str):
        check_required_field(payment_link_id, "payment_link_id")
        check_required_field(merchant_id, "merchant_id")

        payload = {
            "id": payment_link_id,
            "merchantId": merchant_id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/disable-subscriber-billing-link",
            payload=payload
        )

    """
    The method allows you to connect a subscription
    
    :param required str merchant_id: Merchant ID in the system
    :param required str billing_link_id: Payment link identifier 
                                         (coins will be debited from the linked address)
    :param required str title: Subscription name
    :param required int spend_interval: Write-off period in minutes. For convenience, 
                                        you can specify: -1 - daily write-off; 
                                        -2 - weekly write-off; -3 - monthly write-off;
    :param required str currency: Payment currency. You can specify a fiat currency or any other, 
                                  the amount will be automatically converted to the currency of 
                                  the payment link
    :param required str amount: Payment amount in the specified currency
    :param str description: Subscription description
    :param str webhook_url: Subscription charge notification URL
    :return: dict
    :raise ValueError: if merchant_id, billing_link_id, title, spend_interval, currency or amount 
                       is not provided
    
    :example:
    >>> sdk.recurring_payments.create_subscription(
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a", 
            "2bfbdf44-fb5b-4e75-9962-f28c0594e483", 
            "Premium", 
            -1, 
            "USD", 
            "100"
        )
    """

    def create_subscription(
            self,
            merchant_id: str,
            billing_link_id: str,
            title: str,
            spend_interval: int,
            currency: str,
            amount: str,
            description: str = None,
            webhook_url: str = None,
    ):
        check_required_field(merchant_id, "merchant_id")
        check_required_field(billing_link_id, "billing_link_id")
        check_required_field(title, "title")
        check_required_field(spend_interval, "spend_interval")
        check_required_field(currency, "currency")
        check_required_field(amount, "amount")

        payload = {
            "merchantId": merchant_id,
            "billingLinkId": billing_link_id,
            "title": title,
            "spendInterval": spend_interval,
            "currency": currency,
            "amount": amount,
            "description": description,
            "webhookUrl": webhook_url
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/create-subscription",
            payload=payload
        )

    """
    The method allows you to get information about the subscription
    
    :param required str subscription_id: Subscription ID in the system
    :param required str merchant_id: Merchant ID in the system
    :return: dict
    :raise ValueError: if subscription_id or merchant_id is not provided
    
    :example:
    >>> sdk.recurring_payments.get_subscription(
            "be1179ff-586f-4980-b6ca-7e11a93bb99f", 
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a"
        )
    """

    def get_subscription(self, subscription_id: str, merchant_id: str):
        check_required_field(subscription_id, "subscription_id")
        check_required_field(merchant_id, "merchant_id")

        payload = {
            "id": subscription_id,
            "merchantId": merchant_id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/get-subscription",
            payload=payload
        )

    """
    The method allows you to disable a previously connected subscription
    
    :param required str subscription_id: Subscription ID in the system
    :param required str merchant_id: Merchant ID in the system
    :return: dict
    :raise ValueError: if subscription_id or merchant_id is not provided
    
    :example:
    >>> sdk.recurring_payments.cancel_subscription(
            "be1179ff-586f-4980-b6ca-7e11a93bb99f", 
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a"
        )
    """

    def cancel_subscription(self, subscription_id: str, merchant_id: str):
        check_required_field(subscription_id, "subscription_id")
        check_required_field(merchant_id, "merchant_id")

        payload = {
            "id": subscription_id,
            "merchantId": merchant_id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/cancel-subscription",
            payload=payload
        )

    """
    The method allows you to create a payment with an arbitrary amount in the coin in which 
    the address was connected
    
    :param required str merchant_id: Merchant ID in the system
    :param required str billing_link_id: Payment link identifier 
                                         (coins will be debited from the linked address)
    :param required str amount: Payment amount
    :param str webhook_url: Payment notification URL
    :return: dict
    :raise ValueError: if merchant_id, billing_link_id or amount is not provided
    
    :example:
    >>> sdk.recurring_payments.create_payment(
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a", 
            "2bfbdf44-fb5b-4e75-9962-f28c0594e483", 
            "100"
        )
    """

    def create_payment(
            self,
            merchant_id: str,
            billing_link_id: str,
            amount: str,
            webhook_url: str = None
    ):
        check_required_field(merchant_id, "merchant_id")
        check_required_field(billing_link_id, "billing_link_id")
        check_required_field(amount, "amount")

        payload = {
            "merchantId": merchant_id,
            "billingLinkId": billing_link_id,
            "amount": amount,
            "webhookUrl": webhook_url
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/make-payment",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.RecurringPayments>"
