from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class AddressBook:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    Adding a new address to the address book

    :param required str address: The address in the blockchain
    :param required list networks: List of address networks
    :param required str alias: Address name
    :param str comment: Comment on the address
    :return: dict
    :raise ValueError: if address, networks or alias is not provided

    :example:
    >>> sdk.address_book.add_address(
            "0x6b175474e89094c44da98b954eedeac495271d0f", 
            ["ethereum"], 
            "Alias",
        )
    """

    def add_address(self, address: str, networks: list, alias: str, comment: str = None):
        check_required_field(address, "address")
        check_required_field(networks, "networks")
        check_required_field(alias, "alias")

        payload = {
            "address": address,
            "networks": networks,
            "alias": alias,
            "comment": comment
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/address-book/add",
            payload=payload
        )

    """
    Deleting an address from the address book

    :param required str addressId: The ID of the address in the system
    :return: dict
    :raise ValueError: if addressId is not provided

    :example:
    >>> sdk.address_book.delete_address("cd3867c2-2d55-4bfa-be7e-b2964ccedcc4")
    """

    def delete_address(self, addressId: str):
        check_required_field(addressId, "addressId")

        payload = {
            "addressId": addressId
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/address-book/remove",
            payload=payload
        )

    """
    Updating information at

    :param required str addressId: The ID of the address in the system
    :param required str alias: Address name
    :param str comment: Comment on the address
    :return: dict
    :raise ValueError: if addressId is not provided

    :example:
    >>> sdk.address_book.update_address(
            "cd3867c2-2d55-4bfa-be7e-b2964ccedcc4",
            "Alias #2",
        )
    """

    def update_address(self, addressId: str, alias: str = None, comment: str = None):
        check_required_field(addressId, "addressId")

        payload = {
            "addressId": addressId,
            "alias": alias,
            "comment": comment
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/address-book/update",
            payload=payload
        )

    """
    Getting a list of addresses
    
    :param int limit: Limit (for pagination)
    :param int page: Offset (for pagination)
    :param list networks: List of networks to search for addresses in
    :return: dict
    
    :example:
    >>> sdk.address_book.get_addresses()
    """

    def get_addresses(self, page: int = None, limit: int = 10, networks: list = None):
        payload = {
            "page": page,
            "limit": limit,
            "networks": networks
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/address-book/get",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.AddressBook>"
