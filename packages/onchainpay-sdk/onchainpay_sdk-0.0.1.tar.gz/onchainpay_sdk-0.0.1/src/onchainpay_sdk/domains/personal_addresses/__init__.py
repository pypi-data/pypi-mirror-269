from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class PersonalAddresses:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    This method provides functionality of:
        - creating user
        - updating data of a previously created user when specifying the same clientId. 
          The sent parameter values overwrite the previous data.
        
    :param required str client_id: User ID in the merchant system
    :param str client_email: User email
    :param str client_name: User name
    :param str deposit_webhook_url: URL for notifications of new deposits
    :param bool create_addresses: Create all addresses for the user
    :param bool group_by_blockchain: Group addresses by blockchain networks 
                                    (for example, 1 address for bsc, fantom, ethereum networks). 
                                    This parameter has an effect only when createAddresses: true
    :param bool check_risks: Check risks for every incoming transaction to the user's 
                             personal addresses. Information about risks will be sent in the webhook 
                             to the specified depositWebhookUrl in the risks field
    :return: dict
    :raise ValueError: If client_id is not provided
    
    :example:
    >>> sdk.personal_addresses.create_or_update_user(
            "id123",
            client_email="user@mail.com",
            client_name="User Name",
        )
    """

    def create_or_update_user(
            self,
            client_id: str,
            client_email: str = None,
            client_name: str = None,
            deposit_webhook_url: str = None,
            create_addresses: bool = None,
            group_by_blockchain: bool = None,
            check_risks: bool = False,
    ):
        check_required_field(client_id, "client_id")

        payload = {
            "clientId": client_id,
            "clientEmail": client_email,
            "clientName": client_name,
            "depositWebhookUrl": deposit_webhook_url,
            "createAddresses": create_addresses,
            "groupByBlockchain": group_by_blockchain,
            "checkRisks": check_risks,
        }

        return self.sdk.request(
            "post", self.base_url, path="/personal-addresses/create-user", payload=payload
        )

    """
    By using this method you can:
        - Get the address for the user in the specified coin and network. When the request is 
          repeated, the previously created address is returned, which will have isActive: true
          
        - Generate a new address for the user in the specified coin and network, when specifying 
          the parameter renewAddress. The new address will have isActive: true, previously
          generated addresses with the same coin and network will have isActive: false
    
    Note: At any time, a user can have only one active address in particular coin and network. 
    Deposits and withdrawals work at all addresses, regardless of the parameter isActive

    :param required str user_id: User ID
    :param required str currency: Address coin
    :param required str network: Address network
    :param bool renew_address: If set to true a new address will be issued to the user, 
                               the old one will become inactive
    :return: dict
    :raise ValueError: If user_id, currency, or network is not provided
    
    :example:
    >>> sdk.personal_addresses.get_user_address(
            "463fa3c3-bc26-451a-9eb9-5cb0d7d7c5aa",
            "USDT",
            "ethereum",
        )
    """

    def get_user_address(
            self,
            user_id: str,
            currency: str,
            network: str,
            renew_address: bool = False
    ):
        check_required_field(user_id, "user_id")
        check_required_field(currency, "currency")
        check_required_field(network, "network")

        payload = {
            "id": user_id,
            "currency": currency,
            "network": network,
            "renewAddress": renew_address
        }

        return self.sdk.request(
            "post", self.base_url, path="/personal-addresses/get-user-address", payload=payload
        )

    """
    The method allows you to get all the user's personal addresses. 
    Deposits and withdrawals are available for all addresses, but the user should only see 
    addresses with isActive: true. Thus, if necessary, you can generate a new address for 
    a user in a certain coin and network, then all previous addresses in this coin and 
    network will have the parameter isActive: false (read more in the previous method 
    "Get/Renew personal address")
    
    :param int limit: Limit (for pagination)
    :param int offset: Offset (for pagination)
    :param str user_id: Filter by User ID
    :param bool is_active: Filter by parameter 'isActive'
    :param list currency: Filter by currencies
    :param list network: Filter by networks
    :param dict balance: Filter by balance
    :return: dict
    
    :example:
    >>> sdk.personal_addresses.get_addresses(limit=10, offset=0)
    """

    def get_user_addresses(
            self,
            user_id: str = None,
            currency: list = None,
            network: list = None,
            is_active: bool = None,
            balance: dict = None,
            limit: int = 10,
            offset: int = 0,
    ):
        payload = {
            "limit": limit,
            "offset": offset,
            "id": user_id,
            "isActive": is_active,
            "currency": currency,
            "network": network,
            "balance": balance
        }

        return self.sdk.request(
            "post", self.base_url, path="/personal-addresses/get-user-addresses", payload=payload
        )

    """
    The method allows you to get user data by his id or clientId
    
    :param str user_id: User ID in the system. Required, if 'clientId' was not provided
    :param str client_id: User ID in the merchant system. Required, if 'id' was not provided
    :return: dict
    
    :example:
    >>> sdk.personal_addresses.get_user("463fa3c3-bc26-451a-9eb9-5cb0d7d7c5aa")
    """

    def get_user(self, user_id: str = None, client_id: str = None):
        if not user_id and not client_id:
            raise ValueError("user_id or client_id is required")

        payload = {
            "id": user_id,
            "clientId": client_id
        }

        return self.sdk.request(
            "post", self.base_url, path="/personal-addresses/get-user", payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.PersonalAddresses>"
