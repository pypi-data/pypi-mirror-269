from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class KYT:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method allows you to check the risks of a completed transaction.
    
    :param required str tx: Transaction hash
    :param required str currency: Currency
    :param required str network: Network
    :param required str output_address: Output address
    :param required str direction: Direction
    :return: dict
    :raise ValueError: if tx, currency, network, outputAddress or direction is not provided
    
    :example:
    >>> sdk.kyt.check_transaction_risk(
            "0x00E2453...",
            "USDT",
            "ethereum",
            "0x023434a...",
            "sent"
        )
    """

    def check_transaction_risk(
            self,
            tx: str,
            currency: str,
            network: str,
            outputAddress: str,
            direction: str
    ):
        check_required_field(tx, "tx")
        check_required_field(currency, "currency")
        check_required_field(network, "network")
        check_required_field(outputAddress, "outputAddress")
        check_required_field(direction, "direction")

        payload = {
            "tx": tx,
            "currency": currency,
            "network": network,
            "outputAddress": outputAddress,
            "direction": direction
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/kyt/check-transfer",
            payload=payload
        )

    """
    The method allows you to check the risks of withdrawal before making it.
    
    :param required str address: Address-recipient of coins
    :param required str currency: Coin
    :param required str network: Network
    :param required str amount: Withdrawal amount
    
    :return: dict
    :raise ValueError: if address, currency, network or amount is not provided
    
    :example:
    >>> sdk.kyt.check_withdrawal_risk(
            "0x023434a...",
            "USDT",
            "ethereum",
            "0.1"
        )
    """

    def check_withdrawal_risks(self, address: str, currency: str, network: str, amount: str):
        check_required_field(address, "address")
        check_required_field(currency, "currency")
        check_required_field(network, "network")
        check_required_field(amount, "amount")

        payload = {
            "address": address,
            "currency": currency,
            "network": network,
            "amount": amount
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/kyt/check-withdrawal-address",
            payload=payload
        )

    """
    The method allows you to get information about the risk level of withdrawal to the address
    
    :param required str address: Address-recipient of coins
    :param required str currency: Coin
    :param required str network: Network
    :return: dict
    :raise ValueError: if address, currency or network is not provided
    
    :example:
    >>> sdk.kyt.check_withdrawal_address(
            "0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b",
            "USDT",
            "ethereum"
        )
    """

    def check_withdrawal_address(self, address: str, currency: str, network: str):
        check_required_field(address, "address")
        check_required_field(currency, "currency")
        check_required_field(network, "network")

        payload = {
            "address": address,
            "currency": currency,
            "network": network
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/kyt/withdrawal-address-screening",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.KYT>"
