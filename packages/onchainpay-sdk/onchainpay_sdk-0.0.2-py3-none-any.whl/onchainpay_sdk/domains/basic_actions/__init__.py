from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class BasicActions:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    You can test your signature in x-api-signature within this method.
    
    :return: dict
    
    :example:
    >>> sdk.basic_actions.check_x_api_signature()
    """

    def check_x_api_signature(self):
        return self.sdk.request(
            "post",
            self.base_url,
            path="/test-signature"
        )

    """
    Get list of available currencies for depositing/withdrawing
    
    :return: dict
    
    :example:
    >>> sdk.basic_actions.get_currencies()
    """

    def get_currencies(self):
        return self.sdk.request(
            "post",
            self.base_url,
            path="/available-currencies"
        )

    """
    The method allows you to get the current price of an asset in relation to another
    
    :param required str from_currency: Currency to convert from
    :param required str to_currency: Currency to convert to
    :return: dict
    :raise ValueError: if from_currency or to_currency is not provided
    
    :example:
    >>> sdk.basic_actions.get_current_price("BTC", "USDT")
    """

    def get_currency_price(self, fromCurrency: str, toCurrency: str):
        check_required_field(fromCurrency, "fromCurrency")
        check_required_field(toCurrency, "toCurrency")

        payload = {
            "from": fromCurrency,
            "to": toCurrency
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/price-rate",
            payload=payload
        )

    """
    The method allows you to find an operation in the system by the address 
    of the transaction in the blockchain

    The response will indicate the type of operation, the direction of the transaction, 
    the address that was used for the operation and the body of the operation in the record 
    from the type
    
    :param required str tx: Transaction hash
    :return: dict
    :raise ValueError: if tx is not provided
    
    :example:
    >>> sdk.basic_actions.get_operation_by_tx_hash("0x788529118F2A28C60b9de2Ba0353f5EE4293e044")
    """

    def get_operation_by_tx_hash(self, tx: str):
        check_required_field(tx, "tx")

        payload = {
            "tx": tx
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/operation-by-tx-hash",
            payload=payload
        )

    """
    Check address format within provided network
    
    :param required str address: Address
    :param required str network: Network
    :return: dict
    :raise ValueError: if address or network is not provided
    
    :example:
    >>> sdk.basic_actions.check_address_format("0x788529118F2A28C60b9a0353f5EE4293e044", "ethereum")
    """

    def check_address_format(self, address: str, network: str):
        check_required_field(address, "address")
        check_required_field(network, "network")

        payload = {
            "address": address,
            "network": network
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/utils/validate-address",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.BasicActions>"
