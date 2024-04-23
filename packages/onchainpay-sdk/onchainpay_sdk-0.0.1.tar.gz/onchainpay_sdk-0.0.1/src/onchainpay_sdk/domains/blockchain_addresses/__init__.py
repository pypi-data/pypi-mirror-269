from onchainpay_sdk import Client


class BlockchainAddresses:
    def __init__(self, sdk: Client, base_url):
        self.sdk = sdk
        self.base_url = base_url

    """
    The method allows you to find an address belonging to an organization by its ID, 
    regardless of its type
    
    :param required str address_id: ID of the address in the system
    :return: dict
    :raise ValueError: If address_id is not provided
    
    :example:
    >>> sdk.blockchain_addresses.find_by_id("d56bcbe4-586f-4980-b6ca-6e9f557750e8")
    """

    def get_address_by_id(self, address_id: str):
        if not address_id:
            raise ValueError("address ID is required")

        payload = {"id": address_id}

        return self.sdk.request(
            "post", self.base_url, path="/addresses/find-by-id", payload=payload
        )

    """
    To add a tracking address, you must specify the address itself and the URL for sending 
    notifications about transactions. The address will be monitored on all available networks.
    
    :param required str address: Address in the blockchain
    :param required str webhook_url: URL for notifications when a transaction arrives
    :return: dict
    :raise ValueError: If address or webhook_url is not provided
    
    :example:
    >>> sdk.blockchain_addresses.add_tracking_address(
            "0x788529118F2A28C60b9de2Ba0353f5EE4293e044", 
            "https://merchant.domain/webhooks/transaction"
        )
    """

    def add_transaction_tracking(self, address: str, webhook_url: str):
        if not address:
            raise ValueError("address is required")
        if not webhook_url:
            raise ValueError("webhook_url is required")

        payload = {"address": address, "webhookUrl": webhook_url}

        return self.sdk.request(
            "post", self.base_url, path="/track-addresses/add-address", payload=payload
        )

    """
    The method allows you to find addresses belonging to an organization at an address 
    in the blockchain, regardless of the type and network
    
    :param required str address: Address in the blockchain
    :return: dict
    :raise ValueError: If address is not provided
    
    :example:
    >>> sdk.blockchain_addresses.search_by_address("0x788529118F2A28C60b9de2Ba0353f5EE4293e044")
    """

    def get_address_by_address(self, address: str):
        if not address:
            raise ValueError("address is required")

        payload = {"address": address}

        return self.sdk.request(
            "post", self.base_url, path="/addresses/find-by-address", payload=payload
        )

    """
    The method allows you to set the meta-data for the address. 
    The field type is free, you can set any value
    
    :param required str address_id: ID of the address in the system
    :param any meta: Metadata to be set
    :return: dict
    :raise ValueError: If address_id is not provided
    
    :example:
    >>> sdk.blockchain_addresses.set_meta("d56bcbe4-586f-4980-b6ca-6e9f557750e8", {"key": "value"})
    """

    def set_meta(self, address_id: str, meta: any = None):
        if not address_id:
            raise ValueError("address_id is required")

        payload = {"id": address_id, "meta": meta}

        return self.sdk.request(
            "post", self.base_url, path="/addresses/set-meta", payload=payload
        )

    """
    The method allows you to get a list of transactions at the address.
    
    :param required str address_id: Address ID
    :param str tx_type: Transaction type (deposit, withdrawal)
    :param list status: Array of statuses of a transaction (processed, error, rejected, pending)
    :param int limit: Maximum number of transactions to return 
                      (no less than 100 and no more than 1000, by default 100)
    :param int offset: Number of transactions to skip
    :return: dict
    :raise ValueError: If address_id is not provided
    
    :example:
    >>> sdk.blockchain_addresses.get_transactions("8e2d5033-139f-46d4-b769-4a2d2cee37c4")
    """

    def get_transactions(
            self,
            address_id: str,
            tx_type: str = None,
            status: list = None,
            limit: int = None,
            offset: int = None
    ):

        if not address_id:
            raise ValueError("address_id is required")

        payload = {
            "id": address_id,
            "type": tx_type,
            "status": status,
            "limit": limit,
            "offset": offset
        }

        return self.sdk.request(
            "post", self.base_url, path="/addresses/transactions", payload=payload
        )

    """
    The method allows you to get PayIn address data (address, balance, identifier, etc.)
    
    :param required str balance_id: Advance balance identifier
    :return: dict
    :raise ValueError: If balance_id is not provided
    
    :example:
    >>> sdk.blockchain_addresses.get_payin_addresses("ba5716df-58c4-48f8-9401-68f6069fb4ff")
    """

    def get_payin_addresses(self, balance_id: str):
        if not balance_id:
            raise ValueError("balance_id is required")

        payload = {"advancedBalanceId": balance_id}

        return self.sdk.request(
            "post", self.base_url, path="/account-addresses", payload=payload
        )

    """
    Get business addresses for your advanced balance
    
    :param required str balance_id: Advance balance identifier
    :return: dict
    :raise ValueError: If balance_id is not provided
    
    :example:
    >>> sdk.blockchain_addresses.get_business_addresses("ba5716df-58c4-48f8-9401-68f6069fb4ff")
    """

    def get_business_addresses(self, balance_id: str):
        if not balance_id:
            raise ValueError("balance_id is required")

        payload = {"advancedBalanceId": balance_id}

        return self.sdk.request(
            "post", self.base_url, path="/business-addresses", payload=payload
        )

    """
    Get recurrent addresses for your advanced balance
    
    :param required str balance_id: Advance balance identifier
    :return: dict
    :raise ValueError: If balance_id is not provided
    
    :example:
    >>> sdk.blockchain_addresses.get_recurrent_addresses("ba5716df-58c4-48f8-9401-68f6069fb4ff")
    """

    def get_recurrent_addresses(self, balance_id: str):
        if not balance_id:
            raise ValueError("balance_id is required")

        payload = {"advancedBalanceId": balance_id}

        return self.sdk.request(
            "post", self.base_url, path="/recurrent-addresses", payload=payload
        )

    """
    The method allows you to get balances for this account.
    
    :param required str balance_id: Advance balance identifier
    :return: dict
    :raise ValueError: If balance_id is not provided
    
    :example:
    >>> sdk.blockchain_addresses.get_payout_balances("ba5716df-58c4-48f8-9401-68f6069fb4ff")
    """

    def get_payout_addresses(self, balance_id: str):
        if not balance_id:
            raise ValueError("balance_id is required")

        payload = {"advancedBalanceId": balance_id}

        return self.sdk.request(
            "post", self.base_url, path="/payout-balances", payload=payload
        )

    """
    The method allows you to create a new business address.
    
    :param required str balance_id: Advance balance identifier
    :param required str currency: Coin ticker
    :param required str network: Network name
    :param required str alias: Address alias
    :param required str comment: Comment to the address
    :return: dict
    :raise ValueError: If balance_id, currency, network, alias or comment is not provided
    
    :example:
    >>> sdk.blockchain_addresses.create_business_address(
            "ba5716df-58c4-48f8-9401-68f6069fb4ff",
            "USDT",
            "ethereum",
            "My address alias",
            "My some address comment"
        )
    """

    def create_business_address(
            self,
            balance_id: str,
            currency: str,
            network: str,
            alias: str,
            comment: str
    ):
        if not balance_id:
            raise ValueError("balance_id is required")
        if not currency:
            raise ValueError("currency is required")
        if not network:
            raise ValueError("network is required")
        if not alias:
            raise ValueError("alias is required")
        if not comment:
            raise ValueError("comment is required")

        payload = {
            "advancedBalanceId": balance_id,
            "currency": currency,
            "network": network,
            "alias": alias,
            "comment": comment
        }

        return self.sdk.request(
            "post", self.base_url, path="/business-address", payload=payload
        )

    """
    The method allows you to create a new PayOut address.
    
    :param required str currency: Coin ticker
    :param required str network: Network name
    :return: dict
    :raise ValueError: If currency or network is not provided
    
    :example:
    >>> sdk.blockchain_addresses.create_recurrent_address("USDT", "ethereum")
    """

    def create_payout_address(
            self,
            currency: str,
            network: str,
    ):
        if not currency:
            raise ValueError("currency is required")
        if not network:
            raise ValueError("network is required")

        payload = {
            "currency": currency,
            "network": network,
        }

        return self.sdk.request(
            "post", self.base_url, path="/payout-address", payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.BlockchainAddresses>"
