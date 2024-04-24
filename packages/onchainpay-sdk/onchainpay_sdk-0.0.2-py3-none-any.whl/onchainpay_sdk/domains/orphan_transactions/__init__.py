from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class OrphanTransactions:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    Getting information about an orphan transaction by its ID

    :param required str id: Transaction ID in the system
    :return: dict
    :raise ValueError: if id is not provided

    :example:
    >>> sdk.orphan_transactions.get_transaction_by_id("5cbf7135-d75a-4360-a9c4-8de7bf516baa")
    """

    def get_transaction_by_id(self, id: str):
        check_required_field(id, "id")

        payload = {
            "id": id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/orphan-deposits/get-deposit",
            payload=payload
        )

    """
    Getting a list of orphan transactions with the ability to filter by certain criteria

    :param str id: Transaction ID in the system
    :param str orderId: The ID of the order to which the address was linked at the time of 
                         the transaction discovery
    :param str stage: The current stage of the transaction.
    :param str status: Status of the current stage of the transaction
    :param int limit: Number of transactions to return
    :param int offset: Offset for pagination
    :return: dict

    :example:
    >>> sdk.orphan_transactions.get_transactions(
            5cbf7135-d75a-4360-a9c4-8de7bf516baa"
        )
    """

    def get_transactions(
            self,
            id: str = None,
            orderId: str = None,
            stage: str = None,
            status: str = None,
            limit: int = 10,
            offset: int = 0
    ):
        payload = {
            "id": id,
            "orderId": orderId,
            "status": status,
            "stage": stage,
            "limit": limit,
            "offset": offset
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/orphan-deposits/get-deposits",
            payload=payload
        )

    """
    Receiving a commission token to withdraw an orphan transaction
    
    :param required str id: Transaction ID in the system
    :return: dict
    :raise ValueError: if id is not provided
    
    :example:
    >>> sdk.orphan_transactions.get_commission_token("5cbf7135-d75a-4360-a9c4-8de7bf516baa")
    """

    def get_commission_token(self, id: str):
        check_required_field(id, "id")

        payload = {
            "id": id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/orphan-deposits/withdrawal-token",
            payload=payload
        )

    """
    Receiving a commission token to withdraw an orphan transaction
    
    :param required str token: Withdrawal Token
    :param required str address: Output address
    :param str comment: Comment on the conclusion
    :param str webhookUrl: URL for sending a webhook about the withdrawal
    :return: dict
    :raise ValueError: if token or address is not provided
    
    :example:
    >>> sdk.orphan_transactions.get_withdrawal(
            "5cbf7135-d75a-4360-a9c4-8de7bf516baa",
            "0x5cbf7135d75a4360a9c48de7bf516baa"
        )
    """

    def get_withdrawal(
            self,
            token: str,
            address: str,
            comment: str = None,
            webhookUrl: str = None
    ):
        check_required_field(token, "token")
        check_required_field(address, "address")

        payload = {
            "token": token,
            "address": address,
            "comment": comment,
            "webhookUrl": webhookUrl
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/orphan-deposits/withdrawal",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.OrphanTransactions>"
