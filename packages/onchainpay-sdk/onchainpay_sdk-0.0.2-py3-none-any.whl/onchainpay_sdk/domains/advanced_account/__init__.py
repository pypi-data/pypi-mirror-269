from onchainpay_sdk import Client


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

    :return: dict

    :example:
    >>> sdk.advanced_account.get_advanced_balance()
    """

    def get_advanced_balance(self):
        payload = {"advancedBalanceId": self.sdk._advancedBalanceId}

        return self.sdk.request(
            "post", self.base_url, path="/advanced-balances", payload=payload
        )

    """
    Get payment address for advanced balance

    :param str currency: The coin in which you want to replenish the advance balance
    :param str network: The network of the coin in which you want to top up the advance balance
    :return: dict
    :raise ValueError: if network or currency is not provided

    :example:
    >>> sdk.advanced_account.get_payment_address(
            "ethereum", 
            "USDT"
        )
    """

    def get_payment_address(
            self,
            currency: str = None,
            network: str = None
    ):
        payload = {
            "advancedBalanceId": self.sdk._advancedBalanceId,
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
