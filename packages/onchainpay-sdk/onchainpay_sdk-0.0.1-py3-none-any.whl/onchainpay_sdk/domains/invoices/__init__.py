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
    
    :param required str balance_id: Identifier of the advance balance for writing off commissions
    :param required str currency: Coins for payment. You can specify any available coin, 
                                  including fiat. On the invoices page, the amount in the specified 
                                  coin will be recalculated to the coins available for payment
    :param required str amount: Amount payable in the specified coin. On the invoices page, 
                                the amount will be recalculated at the rate of coins 
                                available for payment
    :param required str lifetime: Invoice lifetime in minutes
    :param list currencies: List of coins and networks available for payment, if you specify an 
                            empty array, all coins/networks available in the system will be selected
    :param str external_id: A unique identifier in the merchant's system to prevent 
                            duplication of invoices
    :param str order_id: Order ID in the merchant system
    :param str description: Order Description
    :param bool include_fee: The flag allows you to include the commission of the blockchain 
                             network selected for payment in the amount payable. It will be useful 
                             to lay down your costs for the withdrawal of coins after payment.
    :param list additional_fees: Array with the tariff names, which allows you to include commission 
                                 in final amount for the specified tariffs
    :param str insurance_percent: Allows you to add the specified percentage to the payment amount
    :param str slippage_percent: When opening the invoices page, the user can spend so much time on 
                                 it that the exchange rate changes. If after the transition to 
                                 payment the amount changes more than the specified percentage, 
                                 then the amount payable will be recalculated at the current rate
    :param str webhook_url: URL for notifications when the status of an invoices or amount 
                            received changes
    :param str return_url: URL to specify as "Return to Store" on the checkout page
    :return: dict
    :raise ValueError: If balance_id, currency, amount, or lifetime is not provided
    
    :example:
    >>> sdk.invoices.create_invoice(
            "cfda2034-0944-41c6-98e4-9146e8107dbc",
            "USD",
            "100",
            5,
        )
    """

    def create_invoice(
            self,
            balance_id: str,
            currency: str,
            amount: str,
            lifetime: str,
            currencies: list = None,
            external_id: str = None,
            order_id: str = None,
            description: str = None,
            webhook_url: str = None,
            include_fee: bool = False,
            additional_fees: list = None,
            insurance_percent: str = None,
            slippage_percent: str = None,
            return_url: str = None,
    ):
        check_required_field(balance_id, "balance_id")
        check_required_field(currency, "currency")
        check_required_field(amount, "amount")
        check_required_field(lifetime, "lifetime")

        currencies = currencies or []

        payload = {
            "advancedBalanceId": balance_id,
            "currency": currency,
            "amount": amount,
            "lifetime": lifetime,
            "currencies": currencies,
            "externalId": external_id,
            "order": order_id,
            "description": description,
            "webhookURL": webhook_url,
            "returnURL": return_url,
            "includeFee": include_fee,
            "additionalFees": additional_fees,
            "insurancePercent": insurance_percent,
            "slippagePercent": slippage_percent,
        }

        return self.sdk.request(
            "post", self.base_url, path="/make-invoice", payload=payload
        )

    """
    The method allows you to get information about the invoice
    
    :param required str invoice_id: Invoice ID
    :return: dict
    :raise ValueError: If invoice_id is not provided
    
    :example:
    >>> sdk.invoices.get_invoice_by_id("9f3318d2-66e6-4035-9841-055a83da8974")
    """

    def get_invoice_by_id(self, invoice_id: str):
        check_required_field(invoice_id, "invoice_id")

        payload = {"invoiceId": invoice_id}

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
