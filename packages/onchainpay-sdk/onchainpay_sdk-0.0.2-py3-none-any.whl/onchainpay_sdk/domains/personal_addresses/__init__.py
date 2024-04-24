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
        
    :param required str clientId: User ID in the merchant system
    :param str clientEmail: User email
    :param str clientName: User name
    :param str depositWebhookUrl: URL for notifications of new deposits
    :param bool createAddresses: Create all addresses for the user
    :param bool groupByBlockchain: Group addresses by blockchain networks 
                                    (for example, 1 address for bsc, fantom, ethereum networks). 
                                    This parameter has an effect only when createAddresses: true
    :param bool checkRisks: Check risks for every incoming transaction to the user's 
                             personal addresses. Information about risks will be sent in the webhook 
                             to the specified depositWebhookUrl in the risks field
    :return: dict
    :raise ValueError: If clientId is not provided
    
    :example:
    >>> sdk.personal_addresses.create_or_update_user(
            "id123",
            "user@mail.com",
            "User Name",
        )
    """

    def create_or_update_user(
            self,
            clientId: str,
            clientEmail: str = None,
            clientName: str = None,
            depositWebhookUrl: str = None,
            createAddresses: bool = None,
            groupByBlockchain: bool = None,
            checkRisks: bool = False,
    ):
        check_required_field(clientId, "clientId")

        payload = {
            "clientId": clientId,
            "clientEmail": clientEmail,
            "clientName": clientName,
            "depositWebhookUrl": depositWebhookUrl,
            "createAddresses": createAddresses,
            "groupByBlockchain": groupByBlockchain,
            "checkRisks": checkRisks,
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

    :param required str id: User ID
    :param required str currency: Address coin
    :param required str network: Address network
    :param bool renewAddress: If set to true a new address will be issued to the user, 
                               the old one will become inactive
    :return: dict
    :raise ValueError: If id, currency, or network is not provided
    
    :example:
    >>> sdk.personal_addresses.get_user_address(
            "463fa3c3-bc26-451a-9eb9-5cb0d7d7c5aa",
            "USDT",
            "ethereum",
        )
    """

    def get_user_address(
            self,
            id: str,
            currency: str,
            network: str,
            renewAddress: bool = False
    ):
        check_required_field(id, "id")
        check_required_field(currency, "currency")
        check_required_field(network, "network")

        payload = {
            "id": id,
            "currency": currency,
            "network": network,
            "renewAddress": renewAddress
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
    :param str id: Filter by User ID
    :param bool isActive: Filter by parameter 'isActive'
    :param list currency: Filter by currencies
    :param list network: Filter by networks
    :param dict balance: Filter by balance
    :return: dict
    
    :example:
    >>> sdk.personal_addresses.get_addresses(limit=10, offset=0)
    """

    def get_user_addresses(
            self,
            id: str = None,
            currency: list = None,
            network: list = None,
            isActive: bool = None,
            balance: dict = None,
            limit: int = 10,
            offset: int = 0,
    ):
        payload = {
            "id": id,
            "limit": limit,
            "offset": offset,
            "isActive": isActive,
            "currency": currency,
            "network": network,
            "balance": balance
        }

        return self.sdk.request(
            "post", self.base_url, path="/personal-addresses/get-user-addresses", payload=payload
        )

    """
    The method allows you to get user data by his id or clientId
    
    :param str id: User ID in the system. Required, if 'clientId' was not provided
    :param str clientId: User ID in the merchant system. Required, if 'id' was not provided
    :return: dict
    
    :example:
    >>> sdk.personal_addresses.get_user("463fa3c3-bc26-451a-9eb9-5cb0d7d7c5aa")
    """

    def get_user(self, id: str = None, clientId: str = None):
        if not id and not clientId:
            raise ValueError("id or clientId is required")

        payload = {
            "id": id,
            "clientId": clientId
        }

        return self.sdk.request(
            "post", self.base_url, path="/personal-addresses/get-user", payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.PersonalAddresses>"
