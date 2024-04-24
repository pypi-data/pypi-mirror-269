from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class Invoices:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method allows you to create an invoices for payment without a strict indication 
    of the coin and network, you can specify a payment of 30 USD and a list of 
    coins/networks available for payment, the user himself will choose what is 
    more convenient for him to pay. 
    The amount will be automatically converted to the selected coin for payment
    
    :param required str currency: Coins for payment. You can specify any available coin, 
                                  including fiat. On the invoices page, the amount in the specified 
                                  coin will be recalculated to the coins available for payment
    :param required str amount: Amount payable in the specified coin. On the invoices page, 
                                the amount will be recalculated at the rate of coins 
                                available for payment
    :param required str lifetime: Invoice lifetime in minutes
    :param list currencies: List of coins and networks available for payment, if you specify an 
                            empty array, all coins/networks available in the system will be selected
    :param str externalId: A unique identifier in the merchant's system to prevent 
                            duplication of invoices
    :param str order: Order ID in the merchant system
    :param str description: Order Description
    :param bool includeFee: The flag allows you to include the commission of the blockchain 
                             network selected for payment in the amount payable. It will be useful 
                             to lay down your costs for the withdrawal of coins after payment.
    :param list additionalFees: Array with the tariff names, which allows you to include commission 
                                 in final amount for the specified tariffs
    :param str insurancePercent: Allows you to add the specified percentage to the payment amount
    :param str slippagePercent: When opening the invoices page, the user can spend so much time on 
                                 it that the exchange rate changes. If after the transition to 
                                 payment the amount changes more than the specified percentage, 
                                 then the amount payable will be recalculated at the current rate
    :param str webhookURL: URL for notifications when the status of an invoices or amount 
                            received changes
    :param str returnURL: URL to specify as "Return to Store" on the checkout page
    :return: dict
    :raise ValueError: If currency, amount, or lifetime is not provided
    
    :example:
    >>> sdk.invoices.create_invoice(
            "USD",
            "100",
            5,
        )
    """

    def create_invoice(
            self,
            currency: str,
            amount: str,
            lifetime: str,
            currencies: list = None,
            externalId: str = None,
            order: str = None,
            description: str = None,
            webhookURL: str = None,
            includeFee: bool = False,
            additionalFees: list = None,
            insurancePercent: str = None,
            slippagePercent: str = None,
            returnURL: str = None,
    ):
        check_required_field(currency, "currency")
        check_required_field(amount, "amount")
        check_required_field(lifetime, "lifetime")

        currencies = currencies or []

        payload = {
            "advancedBalanceId": self.sdk._advancedBalanceId,
            "currency": currency,
            "amount": amount,
            "lifetime": lifetime,
            "currencies": currencies,
            "externalId": externalId,
            "order": order,
            "description": description,
            "webhookURL": webhookURL,
            "returnURL": returnURL,
            "includeFee": includeFee,
            "additionalFees": additionalFees,
            "insurancePercent": insurancePercent,
            "slippagePercent": slippagePercent,
        }

        return self.sdk.request(
            "post", self.base_url, path="/make-invoice", payload=payload
        )

    """
    The method allows you to get information about the invoice
    
    :param required str invoiceId: Invoice ID
    :return: dict
    :raise ValueError: If invoiceId is not provided
    
    :example:
    >>> sdk.invoices.get_invoice_by_id("9f3318d2-66e6-4035-9841-055a83da8974")
    """

    def get_invoice_by_id(self, invoiceId: str):
        check_required_field(invoiceId, "invoiceId")

        payload = {"invoiceId": invoiceId}

        return self.sdk.request(
            "post", self.base_url, path="/get-invoice", payload=payload
        )

    """
    The method allows you to get a list of invoices
    
    :param int limit: Number of elements per page
    :param int offset: Number of items to skip
    :param list status: Array for filtering orders by status. 
                   Possible values: CREATED, INIT, PENDING, PROCESSED, PARTIAL, 
                                    REJECTED, ERROR, EXPIRED, OVERPAID
    :return: dict
    
    :example:
    >>> sdk.invoices.get_invoices(10, 0, ["CREATED", "INIT"])
    """

    def get_invoices(self, limit: int = 10, offset: int = 0, status: list = None):
        payload = {
            "status": status,
            "limit": limit,
            "offset": offset
        }

        return self.sdk.request(
            "post", self.base_url, path="/get-invoices", payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.Invoices>"
