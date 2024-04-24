from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class CrosschainSwaps:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method allows you to get a commission token for cross-chain exchange
    
    :param required str currencyFrom: Outgoing coin
    :param required str currencyTo: Expected coin
    :param required str networkFrom: Outgoing network
    :param required str networkTo: Expected Network
    :param str amountFrom: Exchange amount
    :param str amountTo: Expected amount
    :return: dict
    :raise ValueError: If currencyFrom, currencyTo, networkFrom, networkTo 
                           or either amountFrom or amountTo is not provided
    
    :example:
    >>> sdk.crosschain_swaps.get_commission_token(
            "USDT",
            "USDT",
            "ethereum",
            "tron",
            "100"
        )
    """

    def get_commission_token(
            self,
            currencyFrom: str,
            currencyTo: str,
            networkFrom: str,
            networkTo: str,
            amountFrom: str = None,
            amountTo: str = None
    ):
        check_required_field(currencyFrom, "currencyFrom")
        check_required_field(currencyTo, "currencyTo")
        check_required_field(networkFrom, "networkFrom")
        check_required_field(networkTo, "networkTo")

        payload = {
            "advancedBalanceId": self.sdk._advancedBalanceId,
            "currencyFrom": currencyFrom,
            "currencyTo": currencyTo,
            "networkFrom": networkFrom,
            "networkTo": networkTo,
        }

        if amountFrom:
            payload["amountFrom"] = amountFrom
        elif amountTo:
            payload["amountTo"] = amountTo
        else:
            raise ValueError("You must provide either amountFrom or amountTo")

        return self.sdk.request(
            "post",
            self.base_url,
            path="/swaps/fee-token",
            payload=payload
        )

    """
    The method allows you to get limits for the amount of blockchain exchange
    
    :return: dict
    
    :example:
    >>> sdk.crosschain_swaps.get_limits()
    """

    def get_limits(self):
        return self.sdk.request(
            "post",
            self.base_url,
            path="/swaps/limit"
        )

    """
    The method allows you to get information on a previously created cross-chain exchange
    
    :param required str id: Swap ID
    :return: dict
    :raise ValueError: If id is not provided
    
    :example:
    >>> sdk.crosschain_swaps.get_transfer_by_id("de2b4697-c758-4759-aa87-218a486589c7")
    """

    def get_swap_by_id(self, id: str):
        check_required_field(id, "id")

        payload = {
            "id": id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/swaps/get", payload=payload
        )

    """
    The method allows you to create a cross-chain exchange. 
    Cross-chain exchange allows you to exchange one asset for another
    
    :param required str addressFromId: Identifier of the outgoing address from which the specified
                                         amount will be debited
    :param required str addressToId: Identifier of the destination address where the coins will be
                                       credited after the swap
    :param required str feeToken: Commission token
    :param str clientId: Unique exchange identifier in the merchant system 
                          (to prevent duplicate requests)
    :param str webhookUrl: URL address for operation status notification
    :return: dict
    :raise ValueError: If addressFromId, addressToId or feeToken is not provided
    
    :example:
    >>> sdk.crosschain_swaps.create_transfer(
            "8e2d5033-139f-46d4-b769-4a2d2cee37c4",
            "0841afb1-f5a6-40c5-a2ff-881783c6e343",
            "U2FsdGVkX1/aencnde88lDxK7r/ySMC1dmw80rLIXoQ0kk/l5EG48/G8Ms8CuY6fYyxPVNw38lBCAWt/mTaQ
            he2pKhC01Vxk/PcuwApgjZUy1d7E3nEggxJVwBCmhvx0yCxGzrBEFhs41LIdJjaif0uMYWrDyEeaC0vyjVp1BPX
            k5rBjgJiIJveEfWgN0EItxRCjPl6A0TpC9KS2B0xCu0MP+eZ+Ve/8HC6KCS1SzHU=",
        )
    """

    def create_swap(
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
            path="/swaps/create",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.CrosschainSwaps>"
