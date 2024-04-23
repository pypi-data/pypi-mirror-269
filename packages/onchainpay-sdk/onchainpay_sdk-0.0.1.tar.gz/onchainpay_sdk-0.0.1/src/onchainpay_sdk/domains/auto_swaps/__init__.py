from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class AutoSwaps:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method create auto-swap request
    Amount limits apply to creation:
        - the amount must be more than $30 in equivalent
        - the amount must be twice the commission of the network of the final coin/network
    
    :param required str address: The address to receive
    :param required str currency: The coin you want to receive
    :param required str network: The network where you want to receive coins
    :param str amount_from: Outgoing amount
    :param str amount_to: The final amount
    :param bool fee_in_amount: To include the network commission in the amount to swap, 
                               when specifying this parameter, the amountTo will be equal to the 
                               amount that the address will receive
    :param str webhook_url: URL for sending a status change notification
    :return: dict
    :raise ValueError: If address, currency, or network is not provided
    
    :example:
    >>> sdk.auto_swaps.create_swap(
            "1CGuTUAx7icKniPVKGiyiT7QLycpkxULLP", 
            "BTC", 
            "bitcoin", 
            "0.1", 
        )
    """

    def create_swap(
            self,
            address: str,
            currency: str,
            network: str,
            amount_from: str = None,
            amount_to: str = None,
            fee_in_amount: bool = None,
            webhook_url: str = None,
    ):
        check_required_field(address, "address")
        check_required_field(currency, "currency")
        check_required_field(network, "network")

        if amount_from is None and amount_to is None:
            raise ValueError("amount_from or amount_to is required")

        payload = {
            "address": address,
            "currency": currency,
            "network": network,
            "amountFrom": amount_from,
            "amountTo": amount_to,
            "feeInAmount": fee_in_amount,
            "webhookUrl": webhook_url
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/auto-swaps/create",
            payload=payload
        )

    """
    Getting auto-swap data by its ID
    
    :param required str swap_id: Auto-swap ID
    :return: dict
    :raise ValueError: If swap_id is not provided
    
    :example:
    >>> sdk.auto_swaps.get_swap_by_id("18f36b77-bb02-4517-a548-d3989917e784")
    """

    def get_swap_by_id(self, swap_id: str):
        check_required_field(swap_id, "swap_id")

        payload = {
            "id": swap_id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/auto-swaps/get", payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.AutoSwaps>"
