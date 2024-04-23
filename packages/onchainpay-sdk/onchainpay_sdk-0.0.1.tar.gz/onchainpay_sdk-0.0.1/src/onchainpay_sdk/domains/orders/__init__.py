from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class Orders:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    Create an order for payment
    
    :param required str balance_id: Identifier of the advance balance for writing off commissions
    :param required str currency: Ticker of the coins in which the payment will be made
    :param required str network: The network of the coin in which the payment will be made
    :param required str amount: Payment amount
    :param required str order_id: Order ID in the merchant system
    :param required int lifetime: Order lifetime in seconds, available values from 1800 (30 minutes) 
                                  to 43200 (12 hours)
    :param str error_url: URL to send webhook on error or order expiration
    :param str success_url: URL to send webhook on successful payment
    :param str return_url: URL to be placed on the payment page as "Return to Store" links
    :param str description: Order description
    :param bool check_risks: Whether to check incoming transactions for this order
    :return: dict
    :raise ValueError: If balance_id, currency, network, amount, order_id, or lifetime 
                            is not provided
    
    :example:
    >>> sdk.orders.create_order(
            "8e2d5033-139f-46d4-b769-4a2d2cee37c4",
            "USDT",
            "ethereum",
            "0.0001",
            "order-1234",
            3600,
        )
    """

    def create_order(
            self,
            balance_id: str,
            currency: str,
            network: str,
            amount: str,
            order_id: str,
            lifetime: int,
            error_url: str = None,
            success_url: str = None,
            return_url: str = None,
            description: str = None,
            check_risks: bool = False
    ):
        check_required_field("balance_id", balance_id)
        check_required_field("currency", currency)
        check_required_field("network", network)
        check_required_field("amount", amount)
        check_required_field("order_id", order_id)
        check_required_field("lifetime", lifetime)

        payload = {
            "advancedBalanceId": balance_id,
            "currency": currency,
            "network": network,
            "amount": amount,
            "order": order_id,
            "lifetime": lifetime,
            "errorWebhook": error_url,
            "successWebhook": success_url,
            "returnUrl": return_url,
            "description": description,
            "checkRisks": check_risks
        }

        return self.sdk.request(
            "post", self.base_url, path="/make-order", payload=payload
        )

    """
    The method allows you to get information on a previously created order 
    by its identifier in the system
    
    :param required str order_id: Order ID in the system
    :return: dict
    :raise ValueError: If order_id is not provided
    
    :example:
    >>> sdk.orders.get_order_by_id("8e2d5033-139f-46d4-b769-4a2d2cee37c4")
    """

    def get_order_by_id(self, order_id: str):
        check_required_field("order_id", order_id)

        payload = {
            "orderId": order_id
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
