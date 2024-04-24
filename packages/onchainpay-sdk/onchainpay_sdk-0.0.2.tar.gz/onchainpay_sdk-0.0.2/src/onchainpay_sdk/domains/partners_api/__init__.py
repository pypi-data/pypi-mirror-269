from onchainpay_sdk import Client
from onchainpay_sdk.resources.utils import check_required_field


class PartnersApi:
    def __init__(self, sdk: Client, base_url):
        self.base_url = base_url
        self.sdk = sdk

    """
    The method allows you to create a user. 
    
    :param required str email: User's email
    :return: dict
    :raise ValueError: if email is not provided
    
    :example:
    >>> sdk.partners_api.create_user("mail@example.com")
    """

    def create_user(self, email: str):
        check_required_field(email, "email")

        payload = {
            "email": email
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/create-user",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to get the user
    
    :param required str id: User ID
    :return: dict
    :raise ValueError: if id is not provided
    
    :example:
    >>> sdk.partners_api.get_user("8efa4a83-86c9-4eb9-899a-27ce1079a2f8")
    """

    def get_user_by_id(self, id: str):
        check_required_field(id, "id")

        payload = {
            "id": id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-user",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to get all users
    
    :param int limit: Number of elements per page
    :param int offset: Number of items to skip
    :return: dict
    
    :example:
    >>> sdk.partners_api.get_users()
    """

    def get_users(self, limit: int = 10, offset: int = 0):
        payload = {
            "limit": limit,
            "offset": offset
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-users",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to create an organization for the user
    
    :param required str userId: User ID
    :return: dict
    :raise ValueError: if userId is not provided
    
    :example:
    >>> sdk.partners_api.create_organization("8efa4a83-86c9-4eb9-899a-27ce1079a2f8")
    """

    def create_organization(self, userId: str, name: str):
        check_required_field(userId, "userId")

        payload = {
            "userId": userId,
            "name": name
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/create-user-organization",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to get a list of organizations
    
    :param required str userId: User ID
    :param int limit: Number of elements per page
    :param int offset: Number of items to skip
    :return: dict
    :raise ValueError: if userId is not provided
    
    :example:
    >>> sdk.partners_api.get_organizations("8efa4a83-86c9-4eb9-899a-27ce1079a2f8")
    """

    def get_organizations(self, userId: str, limit: int = 10, offset: int = 0):
        check_required_field(userId, "userId")

        payload = {
            "userId": userId,
            "limit": limit,
            "offset": offset
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-user-organizations",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to get user's advanced balances
    
    :param required str userId: User ID
    :param required str organizationId: Organization ID
    :return: dict
    :raise ValueError: if userId is not provided
    
    :example:
    >>> sdk.partners_api.get_user_advanced_balance(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8",
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33"
        )
    """

    def get_user_advanced_balance(self, userId: str, organizationId: str):
        check_required_field(userId, "userId")
        check_required_field(organizationId, "organizationId")

        payload = {
            "userId": userId,
            "organizationId": organizationId,
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-organization-advanced-balance",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to top up the user's advance balance
    
    :param required str userId: User ID
    :param required str organizationId: Organization ID
    :param required str balance_id: ID of the advance balance
    :param required str amount: The amount for which the balance is replenished
    :return: dict
    :raise ValueError: if userId, organizationId, balance_id, amount are not provided
    
    :example:
    >>> sdk.partners_api.replenish_user_balance(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8", 
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33", 
            "100"
        )
    """

    def replenish_user_balance(
            self,
            userId: str,
            organizationId: str,
            amount: str
    ):
        check_required_field(userId, "userId")
        check_required_field(organizationId, "organizationId")
        check_required_field(amount, "amount")

        payload = {
            "advancedBalanceId": self.sdk._advancedBalanceId,
            "userId": userId,
            "organizationId": organizationId,
            "amount": amount
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/top-up-advanced-balance",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to get all the general rates on the service. 
    If an individual tariff is not specified for the user, then the general tariff for all users 
    is applied when the commission is deducted
    
    :return: dict
    
    :example:
    >>> sdk.partners_api.get_general_tariffs()
    """

    def get_general_tariffs(self):
        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-default-tariffs",
            api_type="partners"
        )

    """
    The method allows you to create or update an individual tariff.

    If a tariff already exists for this userId and action, then the rest of the specified d
    ata will overwrite this tariff
    
    :param required str userId: User ID
    :param required str organizationId: Organization ID
    :param required str action: Target action on the tariff
    :param required str amount: The commission percentage of the transaction amount (for example, 
                                0.01 means a commission of 1% of the transaction amount)
    :param required str type: Type of fare amount
    :param str comment: Tariff Comment
    :param str minAmount: Minimum commission for debiting (for example, when performing an 
                           operation, 1% of the transaction amount will be debited, but not less 
                           than MinAmount)
    :param str maxAmount: The maximum commission for debiting (for example, when performing an 
                           operation, 1% of the transaction amount will be debited, but no more 
                           than MaxAmount)
    :return: dict
    :raise ValueError: if userId, action, amount, type are not provided
    
    :example:
    >>> sdk.partners_api.create_or_update_user_tariffs(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8", 
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33", 
            "INTERNAL_TRANSFER", 
            "100",
            "PERCENT"
        )
    """

    def create_or_update_organization_tariff(
            self,
            userId: str,
            organizationId: str,
            action: str,
            amount: str,
            type: str,
            comment: str = None,
            minAmount: str = None,
            maxAmount: str = None
    ):
        check_required_field(userId, "userId")
        check_required_field(organizationId, "organizationId")
        check_required_field(action, "action")
        check_required_field(amount, "amount")
        check_required_field(type, "type")

        payload = {
            "userId": userId,
            "organizationId": organizationId,
            "action": action,
            "amount": amount,
            "type": type,
            "comment": comment,
            "minAmount": minAmount,
            "maxAmount": maxAmount
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/set-organization-tariff",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to get all individual tariffs. If an individual tariff is specified 
    for the user, the commission for the specified operation will be charged according to the 
    individual tariff
    
    :param required str userId: User ID
    :param required str organizationId: Organization ID
    :return: dict
    :raise ValueError: if userId, organizationId are not provided
    
    :example:
    >>> sdk.partners_api.get_organization_tariffs(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8", 
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33"
        )
    """

    def get_organization_tariffs(self, userId: str, organizationId: str):
        check_required_field(userId, "userId")
        check_required_field(organizationId, "organizationId")

        payload = {
            "userId": userId,
            "organizationId": organizationId
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-organization-tariffs",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to create an API key for the user
    
    :param required str userId: User ID
    :param required str organizationId: Organization ID
    :param required str alias: API key name
    :return: dict
    :raise ValueError: if userId, organizationId, alias are not provided
    
    :example:
    >>> sdk.partners_api.create_api_key(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8", 
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33", 
            "Integration key"
        )
    """

    def create_api_key(self, userId: str, organizationId: str, alias: str):
        check_required_field(userId, "userId")
        check_required_field(organizationId, "organizationId")
        check_required_field(alias, "alias")

        payload = {
            "userId": userId,
            "organizationId": organizationId,
            "alias": alias
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/create-api-keys",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to get user's API keys
    
    :param required str userId: User ID
    :param required str organizationId: Organization ID
    :param int limit: Number of elements per page
    :param int offset: Number of items to skip
    :return: dict
    :raise ValueError: if userId is not provided
    
    :example:
    >>> sdk.partners_api.get_api_keys("8efa4a83-86c9-4eb9-899a-27ce1079a2f8")
    """

    def get_api_keys(self, userId: str, organizationId: str, limit: int = 10, offset: int = 0):
        check_required_field(userId, "userId")

        payload = {
            "userId": userId,
            "organizationId": organizationId,
            "limit": limit,
            "offset": offset
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-api-keys",
            payload=payload,
            api_type="partners"
        )

    """
    The method allows you to delete the user's API key
    
    :param required str userId: User ID
    :param required str organizationId: Organization ID
    :param required str keyId: API key ID
    :return: dict
    :raise ValueError: if userId, organizationId, keyId are not provided
    
    :example:
    >>> sdk.partners_api.delete_api_key(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8", 
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33", 
            "a9053678-a307-4b05-9ba6-c045dea445f2"
        )
    """

    def delete_api_key(self, userId: str, organizationId: str, keyId: str):
        check_required_field(userId, "userId")
        check_required_field(organizationId, "organizationId")
        check_required_field(keyId, "keyId")

        payload = {
            "userId": userId,
            "organizationId": organizationId,
            "keyId": keyId,
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/delete-api-keys",
            payload=payload,
            api_type="partners"
        )

    def __repr__(self):
        return "<onchainpay_sdk.PartnersApi>"
