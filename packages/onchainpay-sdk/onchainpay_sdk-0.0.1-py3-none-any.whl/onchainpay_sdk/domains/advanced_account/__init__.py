from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class AdvancedAccount:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    Get list of advanced balances of user

    :return: dict

    :example:
    >>> sdk.advanced_account.get_all_advanced_balances()
    """

    def get_advanced_balances(self):
        return self.sdk.request(
            "post", self.base_url, path="/advanced-balances"
        )

    """
    Get info about advanced balance by its id

    :param required str balance_id: Advance balance identifier
    :return: dict
    :raise ValueError: if balance_id is not provided

    :example:
    >>> sdk.advanced_account.get_advanced_address_by_id("ba5716df-58c4-48f8-9401-68f6069fb4ff")
    """

    def get_advanced_address_by_id(self, balance_id: str):
        check_required_field(balance_id, "balance_id")

        payload = {"advancedBalanceId": balance_id}

        return self.sdk.request(
            "post", self.base_url, path="/advanced-balances", payload=payload
        )

    """
    Get payment address for advanced balance

    :param required str balance_id: Advance balance identifier
    :param str currency: The coin in which you want to replenish the advance balance
    :param str network: The network of the coin in which you want to top up the advance balance
    :return: dict
    :raise ValueError: if balance_id, network or currency is not provided

    :example:
    >>> sdk.advanced_account.get_payment_address(
            "ba5716df-58c4-48f8-9401-68f6069fb4ff", 
            "ethereum", 
            "USDT"
        )
    """

    def get_payment_address(self, balance_id: str, currency: str = None, network: str = None):
        check_required_field(balance_id, "balance_id")

        payload = {
            "advancedBalanceId": balance_id,
            "currency": currency,
            "network": network
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/advanced-balance-deposit-address",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.AdvancedBalance>"
