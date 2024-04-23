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
            payload=payload
        )

    """
    The method allows you to get the user
    
    :param required str user_id: User ID
    :return: dict
    :raise ValueError: if user_id is not provided
    
    :example:
    >>> sdk.partners_api.get_user("8efa4a83-86c9-4eb9-899a-27ce1079a2f8")
    """

    def get_user_by_id(self, user_id: str):
        check_required_field(user_id, "user_id")

        payload = {
            "id": user_id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-user",
            payload=payload
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
            payload=payload
        )

    """
    The method allows you to create an organization for the user
    
    :param required str user_id: User ID
    :return: dict
    :raise ValueError: if user_id is not provided
    
    :example:
    >>> sdk.partners_api.create_organization("8efa4a83-86c9-4eb9-899a-27ce1079a2f8")
    """

    def create_organization(self, user_id: str, name: str):
        check_required_field(user_id, "user_id")

        payload = {
            "userId": user_id,
            "name": name
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/create-user-organization",
            payload=payload
        )

    """
    The method allows you to get a list of organizations
    
    :param required str user_id: User ID
    :param int limit: Number of elements per page
    :param int offset: Number of items to skip
    :return: dict
    :raise ValueError: if user_id is not provided
    
    :example:
    >>> sdk.partners_api.get_organizations("8efa4a83-86c9-4eb9-899a-27ce1079a2f8")
    """

    def get_organizations(self, user_id: str, limit: int = 10, offset: int = 0):
        check_required_field(user_id, "user_id")

        payload = {
            "userId": user_id,
            "limit": limit,
            "offset": offset
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-user-organizations",
            payload=payload
        )

    """
    The method allows you to get user's advanced balances
    
    :param required str user_id: User ID
    :param required str organization_id: Organization ID
    :return: dict
    :raise ValueError: if user_id is not provided
    
    :example:
    >>> sdk.partners_api.get_user_advanced_balance(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8",
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33"
        )
    """

    def get_user_advanced_balance(self, user_id: str, organization_id: str):
        check_required_field(user_id, "user_id")
        check_required_field(organization_id, "organization_id")

        payload = {
            "userId": user_id,
            "organizationId": organization_id,
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-organization-advanced-balance",
            payload=payload
        )

    """
    The method allows you to top up the user's advance balance
    
    :param required str user_id: User ID
    :param required str organization_id: Organization ID
    :param required str balance_id: ID of the advance balance
    :param required str amount: The amount for which the balance is replenished
    :return: dict
    :raise ValueError: if user_id, organization_id, balance_id, amount are not provided
    
    :example:
    >>> sdk.partners_api.replenish_user_balance(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8", 
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33", 
            "a9053678-a307-4b05-9ba6-c045dea445f2", 
            "100"
        )
    """

    def replenish_user_balance(
            self,
            user_id: str,
            organization_id: str,
            balance_id: str,
            amount: str
    ):
        check_required_field(user_id, "user_id")
        check_required_field(organization_id, "organization_id")
        check_required_field(balance_id, "balance_id")
        check_required_field(amount, "amount")

        payload = {
            "userId": user_id,
            "organizationId": organization_id,
            "advancedBalanceId": balance_id,
            "amount": amount
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/top-up-advanced-balance",
            payload=payload
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
            path="/get-default-tariffs"
        )

    """
    The method allows you to create or update an individual tariff.

    If a tariff already exists for this userId and action, then the rest of the specified d
    ata will overwrite this tariff
    
    :param required str user_id: User ID
    :param required str organization_id: Organization ID
    :param required str action: Target action on the tariff
    :param required str amount: The commission percentage of the transaction amount (for example, 
                                0.01 means a commission of 1% of the transaction amount)
    :param required str tariff_type: Type of fare amount
    :param str comment: Tariff Comment
    :param str min_amount: Minimum commission for debiting (for example, when performing an 
                           operation, 1% of the transaction amount will be debited, but not less 
                           than MinAmount)
    :param str max_amount: The maximum commission for debiting (for example, when performing an 
                           operation, 1% of the transaction amount will be debited, but no more 
                           than MaxAmount)
    :return: dict
    :raise ValueError: if user_id, action, amount, tariff_type are not provided
    
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
            user_id: str,
            organization_id: str,
            action: str,
            amount: str,
            tariff_type: str,
            comment: str = None,
            min_amount: str = None,
            max_amount: str = None
    ):
        check_required_field(user_id, "user_id")
        check_required_field(organization_id, "organization_id")
        check_required_field(action, "action")
        check_required_field(amount, "amount")
        check_required_field(tariff_type, "tariff_type")

        payload = {
            "userId": user_id,
            "organizationId": organization_id,
            "action": action,
            "amount": amount,
            "type": tariff_type,
            "comment": comment,
            "minAmount": min_amount,
            "maxAmount": max_amount
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/set-organization-tariff",
            payload=payload
        )

    """
    The method allows you to get all individual tariffs. If an individual tariff is specified 
    for the user, the commission for the specified operation will be charged according to the 
    individual tariff
    
    :param required str user_id: User ID
    :param required str organization_id: Organization ID
    :return: dict
    :raise ValueError: if user_id, organization_id are not provided
    
    :example:
    >>> sdk.partners_api.get_organization_tariffs(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8", 
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33"
        )
    """

    def get_organization_tariffs(self, user_id: str, organization_id: str):
        check_required_field(user_id, "user_id")
        check_required_field(organization_id, "organization_id")

        payload = {
            "userId": user_id,
            "organizationId": organization_id
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-organization-tariffs",
            payload=payload
        )

    """
    The method allows you to create an API key for the user
    
    :param required str user_id: User ID
    :param required str organization_id: Organization ID
    :param required str alias: API key name
    :return: dict
    :raise ValueError: if user_id, organization_id, alias are not provided
    
    :example:
    >>> sdk.partners_api.create_api_key(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8", 
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33", 
            "Integration key"
        )
    """

    def create_api_key(self, user_id: str, organization_id: str, alias: str):
        check_required_field(user_id, "user_id")
        check_required_field(organization_id, "organization_id")
        check_required_field(alias, "alias")

        payload = {
            "userId": user_id,
            "organizationId": organization_id,
            "alias": alias
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/create-api-keys",
            payload=payload
        )

    """
    The method allows you to get user's API keys
    
    :param required str user_id: User ID
    :param required str organization_id: Organization ID
    :param int limit: Number of elements per page
    :param int offset: Number of items to skip
    :return: dict
    :raise ValueError: if user_id is not provided
    
    :example:
    >>> sdk.partners_api.get_api_keys("8efa4a83-86c9-4eb9-899a-27ce1079a2f8")
    """

    def get_api_keys(self, user_id: str, organization_id: str, limit: int = 10, offset: int = 0):
        check_required_field(user_id, "user_id")

        payload = {
            "userId": user_id,
            "organizationId": organization_id,
            "limit": limit,
            "offset": offset
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/get-api-keys",
            payload=payload
        )

    """
    The method allows you to delete the user's API key
    
    :param required str user_id: User ID
    :param required str organization_id: Organization ID
    :param required str api_key_id: API key ID
    :return: dict
    :raise ValueError: if user_id, organization_id, api_key_id are not provided
    
    :example:
    >>> sdk.partners_api.delete_api_key(
            "8efa4a83-86c9-4eb9-899a-27ce1079a2f8", 
            "e3b5315a-1de9-4b12-9c76-fb79fe4edf33", 
            "a9053678-a307-4b05-9ba6-c045dea445f2"
        )
    """

    def delete_api_key(self, user_id: str, organization_id: str, api_key_id: str):
        check_required_field(user_id, "user_id")
        check_required_field(organization_id, "organization_id")
        check_required_field(api_key_id, "api_key_id")

        payload = {
            "userId": user_id,
            "organizationId": organization_id,
            "keyId": api_key_id,
        }

        return self.sdk.request(
            "post",
            self.base_url,
            path="/delete-api-keys",
            payload=payload
        )

    def __repr__(self):
        return "<onchainpay_sdk.PartnersApi>"
