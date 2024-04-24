from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class Withdraws:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method allows you to get data on the commission that will be debited during the withdrawal
    
    :param required str addressId: Identifier of the address from which you want to withdraw
    :param required str amount: Amount you want to withdraw
    :param bool native: Deduct the gas fee (network fee) from the native balance of the address 
                        (available for payment addresses, PAY_OUT type)
    :return: dict
    :raise ValueError: If addressId, or amount is not provided
    
    :example:
    >>> sdk.withdraws.get_commission_token(
            "8e2d5033-139f-46d4-b769-4a2d2cee37c4",
            "2"
        )
    """

    def get_commission_token(
            self,
            addressId: str,
            amount: str,
            native: bool = None
    ):
        check_required_field(addressId, "addressId")
        check_required_field(amount, "amount")

        payload = {
            "advancedBalanceId": self.sdk._advancedBalanceId,
            "addressId": addressId,
            "amount": amount,
            "native": native,
        }

        return self.sdk.request(
            "post", self.base_url, path="/withdrawal-fee-token", payload=payload
        )

    """
    The method allows you to create a request to withdraw coins from an address
    
    :param required str addressId: Identifier of the address from which the coins 
                                    should be withdrawn
    :param required str address: Address for sending coins
    :param required str amount: Withdrawal amount
    :param required str feeToken: Fee token that was not created when requesting /request-fee
    :param str tag: Tag (memo) address (relevant for networks that support the tag, such as Ripple)
    :return: dict
    :raise ValueError: If addressId, address, amount, or feeToken is not provided
    
    :example:
    >>> sdk.withdraws.create_withdrawal(
            "8e2d5033-139f-46d4-b769-4a2d2cee37c4",
            "0x5b8b7b4b4a2f6c8a6e0b2f2f8e5b2b1c5c6b1c5b",
            "2",
            "0x00000005707Bf50EfA35a2db020eDe9Ac0780b9f"
        )
    """

    def create_withdrawal(
            self,
            addressId: str,
            address: str,
            amount: str,
            feeToken: str,
            tag: str = None
    ):
        check_required_field(addressId, "addressId")
        check_required_field(address, "address")
        check_required_field(amount, "amount")
        check_required_field(feeToken, "feeToken")

        payload = {
            "advancedBalanceId": self.sdk._advancedBalanceId,
            "addressId": addressId,
            "address": address,
            "amount": amount,
            "feeToken": feeToken,
            "tag": tag
        }

        return self.sdk.request(
            "post", self.base_url, path="/make-withdrawal", payload=payload
        )

    """
    The method allows you to create a request to withdraw coins from an address and get the 
    execution result to the specified URL

    :param required str addressId: Identifier of the address from which the coins 
                                    should be withdrawn
    :param required str address: Address for sending coins
    :param required str amount: Withdrawal amount
    :param required str feeToken: Fee token that was not created when requesting /request-fee
    :param str tag: Tag (memo) address (relevant for networks that support the tag, such as Ripple)
    :return: dict
    :raise ValueError: If addressId, address, amount, or feeToken is not provided

    :example:
    >>> sdk.withdraws.create_withdrawal(
            "8e2d5033-139f-46d4-b769-4a2d2cee37c4",
            "0x5b8b7b4b4a2f6c8a6e0b2f2f8e5b2b1c5c6b1c5b",
            "2",
            "0x00000005707Bf50EfA35a2db020eDe9Ac0780b9f",
            "no-tag",
            "https://webhook.site/4e5e1d6b-4c6b-4c6b-4c6b-4c6b4c6b4c6b"
        )
    """

    def create_async_withdrawal(
            self,
            addressId: str,
            address: str,
            amount: str,
            feeToken: str,
            tag: str = None,
            webhookUrl: str = None
    ):
        check_required_field(addressId, "addressId")
        check_required_field(address, "address")
        check_required_field(amount, "amount")
        check_required_field(feeToken, "feeToken")

        payload = {
            "advancedBalanceId": self.sdk._advancedBalanceId,
            "addressId": addressId,
            "address": address,
            "amount": amount,
            "feeToken": feeToken,
            "tag": tag,
            "webhookUrl": webhookUrl
        }

        return self.sdk.request(
            "post", self.base_url, path="/make-withdrawal-async", payload=payload
        )

    """
    The method allows you to get information about the output
    
    :param str withdrawalId: Withdrawal ID in the system
    :return: dict
    :raise ValueError: If withdrawalId is not provided
    
    :example:
    >>> sdk.withdraws.get_withdrawal_by_id("bd6631c2-7f8f-4509-ba4c-418b899465be")
    """

    def get_withdrawal_by_id(self, withdrawalId: str):
        check_required_field(withdrawalId, "withdrawalId")

        payload = {
            "withdrawalId": withdrawalId
        }

        return self.sdk.request(
            "get", self.base_url, path="/get-withdrawal", payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.Withdraws>"
