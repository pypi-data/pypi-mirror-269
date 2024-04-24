from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class CrosschainBridge:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method allows you to get a commission token for cross-chain transfer
    
    :param required str currency: The coin you want to exchange
    :param required str networkFrom: Outgoing network
    :param required str networkTo: Network where you want to receive coins
    :param required str amount: Amount to transfer
    :return: dict
    :raise ValueError: If currency, networkFrom, networkTo or amount 
                           is not provided
    
    :example:
    >>> sdk.crosschain_bridge.get_commission_token(
            "USDT",
            "ethereum",
            "tron",
            "100"
        )
    """

    def get_commission_token(
            self,
            currency: str,
            networkFrom: str,
            networkTo: str,
            amount: str
    ):
        check_required_field(currency, "currency")
        check_required_field(networkFrom, "networkFrom")
        check_required_field(networkTo, "networkTo")
        check_required_field(amount, "amount")

        payload = {
            "advancedBalanceId": self.sdk._advancedBalanceId,
            "currency": currency,
            "networkFrom": networkFrom,
            "networkTo": networkTo,
            "amount": amount
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/bridge/fee-token",
            payload=payload
        )

    """
    The method allows you to get limits for the amount of blockchain transfer
    
    :return: dict
    
    :example:
    >>> sdk.crosschain_bridge.get_limits()
    """

    def get_limits(self):
        return self.sdk.request(
            "post",
            self.base_url,
            path="/bridge/limit"
        )

    """
    The method allows you to get information on a previously created cross-chain transfer
    
    :param required str id: Cross-chain transfer ID
    :return: dict
    :raise ValueError: If id is not provided
    
    :example:
    >>> sdk.crosschain_bridge.get_transfer_by_id("37ca03bc-e0f3-41d8-9ba3-fc214128fe08")
    """

    def get_transfer_by_id(self, id: str):
        check_required_field(id, "id")

        payload = {
            "id": id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/bridge/get", payload=payload
        )

    """
    The method allows you to create a cross-chain transfer. 
    Cross-chain transfer allows you to transfer your assets from one network to another
    

    :param required str addressFromId: Identifier of the outgoing address in the system, 
                                         in the specified coin and network when creating 
                                         the commission token. The specified amount will be 
                                         debited from this address
    :param required str addressToId: Identifier of the destination address in the system 
                                       where the coins should be delivered
    :param required str feeToken: Commission token
    :param str clientId: Unique transaction identifier in the merchant system, 
                          to prevent duplication of creation
    :param str webhookUrl: URL address for operation status notification
    :return: dict
    :raise ValueError: If balance_id, addressFromId, addressToId or feeToken 
                           is not provided
    
    :example:
    >>> sdk.crosschain_bridge.create_transfer(
            "0841afb1-f5a6-40c5-a2ff-881783c6e343",
            "U2FsdGVkX1/aencnde88lDxK7r/ySMC1dmw80rLIXoQ0kk/l5EG48/G8Ms8CuY6fYyxPVNw38lBCAWt/mTaQ
            he2pKhC01Vxk/PcuwApgjZUy1d7E3nEggxJVwBCmhvx0yCxGzrBEFhs41LIdJjaif0uMYWrDyEeaC0vyjVp1BPX
            k5rBjgJiIJveEfWgN0EItxRCjPl6A0TpC9KS2B0xCu0MP+eZ+Ve/8HC6KCS1SzHU=",
        )
    """

    def create_transfer(
            self,
            addressFromId: str,
            addressToId: str,
            feeToken: str,
            clientId: str = None,
            webhookUrl: str = None
    ):
        check_required_field(addressFromId, "addressFromId")
        check_required_field(addressToId, "addressToId")
        check_required_field(feeToken, "feeToken")

        payload = {
            "advancedBalanceId": self.sdk._advancedBalanceId,
            "addressFromId": addressFromId,
            "addressToId": addressToId,
            "feeToken": feeToken,
            "clientId": clientId,
            "webhookUrl": webhookUrl
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/bridge/create",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.CrosschainBridge>"
