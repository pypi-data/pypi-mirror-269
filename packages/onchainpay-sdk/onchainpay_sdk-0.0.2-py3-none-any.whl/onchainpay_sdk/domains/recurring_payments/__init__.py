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
    
    :param required str merchantId: Merchant ID in the system
    :param required str clientId: Client ID in the merchant system
    :param required str clientEmail: Client's mail in the merchant's system
    :param str clientName: Client name in the merchant system
    :param str returnUrl: URL to be used as "Return to Store" link
    :param str webhookUrl: URL to notify about connecting or denying a client's connection request
    :return: dict
    :raise ValueError: if merchantId, clientId or clientEmail is not provided    
    
    :example:
    >>> sdk.recurring_payments.create_payment_link(
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a", 
            "id1234", 
            "maiL@example.com",
        )
    """

    def create_payment_link(
            self,
            merchantId: str,
            clientId: str,
            clientEmail: str,
            clientName: str = None,
            returnUrl: str = None,
            webhookUrl: str = None,
    ):
        check_required_field(merchantId, "merchantId")
        check_required_field(clientId, "clientId")
        check_required_field(clientEmail, "clientEmail")

        payload = {
            "merchantId": merchantId,
            "clientId": clientId,
            "clientEmail": clientEmail,
            "clientName": clientName,
            "returnUrl": returnUrl,
            "webhookUrl": webhookUrl
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/create-subscriber-billing-link",
            payload=payload
        )

    """
    The method allows you to get payment link data
    
    :param required str id: ID of the payment link in the system
    :param required str merchantId: Merchant ID in the system
    :return: dict
    :raise ValueError: if id or merchantId is not provided
    
    :example:
    >>> sdk.recurring_payments.get_payment_link(
        "d56bcbe4-586f-4980-b6ca-6e9f557750e8", 
        "672c1e2d-354f-49a1-8a5b-75af87e92f0a"
    )
    """

    def get_payment_link(self, id: str, merchantId: str):
        check_required_field(id, "id")
        check_required_field(merchantId, "merchantId")

        payload = {
            "id": id,
            "merchantId": merchantId
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/get-billing-link",
            payload=payload
        )

    """
    The method allows you to get a list of payment links for a specific user
    
    :param required str merchantId: Merchant ID in the system
    :param str clientId: Client ID in the merchant system
    :param str clientEmail: Client's mail in the merchant's system
    :return: dict
    :raise ValueError: if merchantId is not provided
    
    :example:
    >>> sdk.recurring_payments.get_payment_links("672c1e2d-354f-49a1-8a5b-75af87e92f0a")
    """

    def get_payment_links(self, merchantId: str, clientId: str = None, clientEmail: str = None):
        check_required_field(merchantId, "merchantId")

        payload = {
            "merchantId": merchantId,
            "clientId": clientId,
            "clientEmail": clientEmail
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
    
    :param required str id: ID of the payment link in the system
    :param required str merchantId: Merchant ID in the system
    :return: dict
    :raise ValueError: if id or merchantId is not provided
    
    :example:
    >>> sdk.recurring_payments.disable_payment_link(
            "d56bcbe4-586f-4980-b6ca-6e9f557750e8", 
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a"
        )
    """

    def disable_payment_link(self, id: str, merchantId: str):
        check_required_field(id, "id")
        check_required_field(merchantId, "merchantId")

        payload = {
            "id": id,
            "merchantId": merchantId
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/disable-subscriber-billing-link",
            payload=payload
        )

    """
    The method allows you to connect a subscription
    
    :param required str merchantId: Merchant ID in the system
    :param required str billingLinkId: Payment link identifier 
                                         (coins will be debited from the linked address)
    :param required str title: Subscription name
    :param required int spendInterval: Write-off period in minutes. For convenience, 
                                        you can specify: -1 - daily write-off; 
                                        -2 - weekly write-off; -3 - monthly write-off;
    :param required str currency: Payment currency. You can specify a fiat currency or any other, 
                                  the amount will be automatically converted to the currency of 
                                  the payment link
    :param required str amount: Payment amount in the specified currency
    :param str description: Subscription description
    :param str webhookUrl: Subscription charge notification URL
    :return: dict
    :raise ValueError: if merchantId, billingLinkId, title, spendInterval, currency or amount 
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
            merchantId: str,
            billingLinkId: str,
            title: str,
            spendInterval: int,
            currency: str,
            amount: str,
            description: str = None,
            webhookUrl: str = None,
    ):
        check_required_field(merchantId, "merchantId")
        check_required_field(billingLinkId, "billingLinkId")
        check_required_field(title, "title")
        check_required_field(spendInterval, "spendInterval")
        check_required_field(currency, "currency")
        check_required_field(amount, "amount")

        payload = {
            "merchantId": merchantId,
            "billingLinkId": billingLinkId,
            "title": title,
            "spendInterval": spendInterval,
            "currency": currency,
            "amount": amount,
            "description": description,
            "webhookUrl": webhookUrl
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/create-subscription",
            payload=payload
        )

    """
    The method allows you to get information about the subscription
    
    :param required str id: Subscription ID in the system
    :param required str merchantId: Merchant ID in the system
    :return: dict
    :raise ValueError: if id or merchantId is not provided
    
    :example:
    >>> sdk.recurring_payments.get_subscription(
            "be1179ff-586f-4980-b6ca-7e11a93bb99f", 
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a"
        )
    """

    def get_subscription(self, id: str, merchantId: str):
        check_required_field(id, "id")
        check_required_field(merchantId, "merchantId")

        payload = {
            "id": id,
            "merchantId": merchantId
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/get-subscription",
            payload=payload
        )

    """
    The method allows you to disable a previously connected subscription
    
    :param required str id: Subscription ID in the system
    :param required str merchantId: Merchant ID in the system
    :return: dict
    :raise ValueError: if id or merchantId is not provided
    
    :example:
    >>> sdk.recurring_payments.cancel_subscription(
            "be1179ff-586f-4980-b6ca-7e11a93bb99f", 
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a"
        )
    """

    def cancel_subscription(self, id: str, merchantId: str):
        check_required_field(id, "id")
        check_required_field(merchantId, "merchantId")

        payload = {
            "id": id,
            "merchantId": merchantId
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
    
    :param required str merchantId: Merchant ID in the system
    :param required str billingLinkId: Payment link identifier 
                                         (coins will be debited from the linked address)
    :param required str amount: Payment amount
    :param str webhookUrl: Payment notification URL
    :return: dict
    :raise ValueError: if merchantId, billingLinkId or amount is not provided
    
    :example:
    >>> sdk.recurring_payments.create_payment(
            "672c1e2d-354f-49a1-8a5b-75af87e92f0a", 
            "2bfbdf44-fb5b-4e75-9962-f28c0594e483", 
            "100"
        )
    """

    def create_payment(
            self,
            merchantId: str,
            billingLinkId: str,
            amount: str,
            webhookUrl: str = None
    ):
        check_required_field(merchantId, "merchantId")
        check_required_field(billingLinkId, "billingLinkId")
        check_required_field(amount, "amount")

        payload = {
            "merchantId": merchantId,
            "billingLinkId": billingLinkId,
            "amount": amount,
            "webhookUrl": webhookUrl
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/recurrents/make-payment",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.RecurringPayments>"
