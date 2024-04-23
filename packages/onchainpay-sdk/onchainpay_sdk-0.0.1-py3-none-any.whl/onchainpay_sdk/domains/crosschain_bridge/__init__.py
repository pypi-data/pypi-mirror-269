from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class CrosschainBridge:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method allows you to get a commission token for cross-chain transfer
    
    :param required str balance_id: Identifier of the advance balance that will act as 
                                    the payer of commissions
    :param required str currency: The coin you want to exchange
    :param required str network_from: Outgoing network
    :param required str network_to: Network where you want to receive coins
    :param required str amount: Amount to transfer
    :return: dict
    :raise ValueError: If balance_id, currency, network_from, network_to or amount 
                           is not provided
    
    :example:
    >>> sdk.crosschain_bridge.get_commission_token(
            "d56bcbe4-586f-4980-b6ca-6e9f557750e8",
            "USDT",
            "ethereum",
            "tron",
            "100"
        )
    """

    def get_commission_token(
            self,
            balance_id: str,
            currency: str,
            network_from: str,
            network_to: str,
            amount: str
    ):
        check_required_field(balance_id, "balance_id")
        check_required_field(currency, "currency")
        check_required_field(network_from, "network_from")
        check_required_field(network_to, "network_to")
        check_required_field(amount, "amount")

        payload = {
            "advancedBalanceId": balance_id,
            "currency": currency,
            "networkFrom": network_from,
            "networkTo": network_to,
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
    
    :param required str transfer_id: Cross-chain transfer ID
    :return: dict
    :raise ValueError: If transfer_id is not provided
    
    :example:
    >>> sdk.crosschain_bridge.get_transfer_by_id("37ca03bc-e0f3-41d8-9ba3-fc214128fe08")
    """

    def get_transfer_by_id(self, transfer_id: str):
        check_required_field(transfer_id, "transfer_id")

        payload = {
            "id": transfer_id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/bridge/get", payload=payload
        )

    """
    The method allows you to create a cross-chain transfer. 
    Cross-chain transfer allows you to transfer your assets from one network to another
    
    :param required str balance_id: Identifier of the advance balance specified when creating 
                                    the commission token 
    :param required str address_from_id: Identifier of the outgoing address in the system, 
                                         in the specified coin and network when creating 
                                         the commission token. The specified amount will be 
                                         debited from this address
    :param required str address_to_id: Identifier of the destination address in the system 
                                       where the coins should be delivered
    :param required str fee_token: Commission token
    :param str client_id: Unique transaction identifier in the merchant system, 
                          to prevent duplication of creation
    :param str webhook_url: URL address for operation status notification
    :return: dict
    :raise ValueError: If balance_id, address_from_id, address_to_id or fee_token 
                           is not provided
    
    :example:
    >>> sdk.crosschain_bridge.create_transfer(
            "ba5716df-58c4-48f8-9401-68f6069fb4ff",
            "8e2d5033-139f-46d4-b769-4a2d2cee37c4",
            "0841afb1-f5a6-40c5-a2ff-881783c6e343",
            "U2FsdGVkX1/aencnde88lDxK7r/ySMC1dmw80rLIXoQ0kk/l5EG48/G8Ms8CuY6fYyxPVNw38lBCAWt/mTaQ
            he2pKhC01Vxk/PcuwApgjZUy1d7E3nEggxJVwBCmhvx0yCxGzrBEFhs41LIdJjaif0uMYWrDyEeaC0vyjVp1BPX
            k5rBjgJiIJveEfWgN0EItxRCjPl6A0TpC9KS2B0xCu0MP+eZ+Ve/8HC6KCS1SzHU=",
        )
    """

    def create_transfer(
            self,
            balance_id: str,
            address_from_id: str,
            address_to_id: str,
            fee_token: str,
            client_id: str = None,
            webhook_url: str = None
    ):
        check_required_field(balance_id, "balance_id")
        check_required_field(address_from_id, "address_from_id")
        check_required_field(address_to_id, "address_to_id")
        check_required_field(fee_token, "fee_token")

        payload = {
            "advancedBalanceId": balance_id,
            "addressFromId": address_from_id,
            "addressToId": address_to_id,
            "feeToken": fee_token,
            "clientId": client_id,
            "webhookUrl": webhook_url
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/bridge/create",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.CrosschainBridge>"
