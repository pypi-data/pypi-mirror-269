from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class Orders:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    Create an order for payment
    
    :param required str currency: Ticker of the coins in which the payment will be made
    :param required str network: The network of the coin in which the payment will be made
    :param required str amount: Payment amount
    :param required str order: Order ID in the merchant system
    :param required int lifetime: Order lifetime in seconds, available values from 1800 (30 minutes) 
                                  to 43200 (12 hours)
    :param str errorWebhook: URL to send webhook on error or order expiration
    :param str successWebhook: URL to send webhook on successful payment
    :param str returnUrl: URL to be placed on the payment page as "Return to Store" links
    :param str description: Order description
    :param bool checkRisks: Whether to check incoming transactions for this order
    :return: dict
    :raise ValueError: If balance_id, currency, network, amount, order, or lifetime is not provided
    
    :example:
    >>> sdk.orders.create_order(
            "USDT",
            "ethereum",
            "0.0001",
            "order-1234",
            3600,
        )
    """

    def create_order(
            self,
            currency: str,
            network: str,
            amount: str,
            order: str,
            lifetime: int,
            errorWebhook: str = None,
            successWebhook: str = None,
            returnUrl: str = None,
            description: str = None,
            checkRisks: bool = False
    ):
        check_required_field("currency", currency)
        check_required_field("network", network)
        check_required_field("amount", amount)
        check_required_field("order", order)
        check_required_field("lifetime", lifetime)

        payload = {
            "advancedBalanceId": self.sdk._advancedBalanceId,
            "currency": currency,
            "network": network,
            "amount": amount,
            "order": order,
            "lifetime": lifetime,
            "errorWebhook": errorWebhook,
            "successWebhook": successWebhook,
            "returnUrl": returnUrl,
            "description": description,
            "checkRisks": checkRisks
        }

        return self.sdk.request(
            "post", self.base_url, path="/make-order", payload=payload
        )

    """
    The method allows you to get information on a previously created order 
    by its identifier in the system
    
    :param required str orderId: Order ID in the system
    :return: dict
    :raise ValueError: If orderId is not provided
    
    :example:
    >>> sdk.orders.get_order_by_id("8e2d5033-139f-46d4-b769-4a2d2cee37c4")
    """

    def get_order_by_id(self, orderId: str):
        check_required_field("orderId", orderId)

        payload = {
            "orderId": orderId
        }

        return self.sdk.request(
            "post", self.base_url, path="/order", payload=payload
        )

    """
    The method allows you to get a list of orders
    
    :param int limit: Number of elements per page
    :param int offset: Number of items to skip
    :param list status: Array for filtering orders by status (init, error, processed, pending, 
                        expired, partial, overpaid)
    :return: dict
    
    :example:
    >>> sdk.orders.get_orders()
    """

    def get_orders(self, limit: int = 100, offset: int = 0, status: list = None):
        payload = {
            "limit": limit,
            "offset": offset,
            "status": status
        }

        return self.sdk.request(
            "post", self.base_url, path="/orders", payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.Orders>"
