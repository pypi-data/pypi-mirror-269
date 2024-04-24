import requests
from onchainpay_sdk.error import AuthenticationError, InternalSDKError
from onchainpay_sdk.resources.requester import APIRequestor


class Client:
    def __init__(self, public_key="", private_key=""):
        if not public_key:
            raise AuthenticationError("Public key is required")
        if not private_key:
            raise AuthenticationError("Private key is required")

        self._base_url = "https://ocp.onchainpay.io/api-gateway"
        self._partners_base_url = "https://ocp.onchainpay.io/partner/api"

        # Domains
        self._advanced_account = None
        self._blockchain_addresses = None
        self._invoices = None
        self._personal_addresses = None
        self._orders = None
        self._withdraws = None
        self._crosschain_bridge = None
        self._crosschain_swaps = None
        self._auto_swaps = None
        self._basic_actions = None
        self._recurring_payments = None
        self._kyt = None
        self._partners_api = None
        self._orphan_transactions = None
        self._address_book = None
        self._webhooks = None

        self._public_key = public_key
        self._private_key = private_key

        self._partners_api_public_key = None
        self._partners_api_private_key = None

        self._advancedBalanceId = None

        self._set_advanced_balance_id()

    def request(
            self,
            method: str,
            base_url: str,
            path: str,
            api_type: str = "public",
            payload: dict = None,
    ):
        if payload and not isinstance(payload, dict):
            raise ValueError("Payload must be a dictionary")

        public_key = self._public_key
        private_key = self._private_key

        if api_type == "partners":
            public_key = self._partners_api_public_key
            private_key = self._partners_api_private_key

        method = method.lower()
        url = f"{base_url}{path}"
        api = APIRequestor(public_key, private_key, url, payload)

        if method == "post":
            response = api.post()
        else:
            raise InternalSDKError("Method not allowed")

        if isinstance(response, dict):
            return response

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return response.text

    def init_partners_api(self, public_key: str, private_key: str):
        if not public_key:
            raise AuthenticationError("Public key is required to initialize partners api")
        if not private_key:
            raise AuthenticationError("Private key is required to initialize partners api")

        self._partners_api_public_key = public_key
        self._partners_api_private_key = private_key

    def _set_advanced_balance_id(self):
        response = self.advanced_account.get_advanced_balances()
        if response.get("success") is True:
            self._advancedBalanceId = response.get("response")[0].get("advancedBalanceId")
        else:
            raise InternalSDKError("Unable to get advanced balance id")

    @property
    def advanced_account(self):
        if self._advanced_account is None:
            from onchainpay_sdk.domains.advanced_account import AdvancedAccount
            self._advanced_account = AdvancedAccount(self, self._base_url)

        return self._advanced_account

    @property
    def blockchain_address(self):
        if self._blockchain_addresses is None:
            from onchainpay_sdk.domains.blockchain_addresses import BlockchainAddresses
            self._blockchain_addresses = BlockchainAddresses(self, self._base_url)

        return self._blockchain_addresses

    @property
    def invoices(self):
        if self._invoices is None:
            from onchainpay_sdk.domains.invoices import Invoices
            self._invoices = Invoices(self, self._base_url)

        return self._invoices

    @property
    def personal_addresses(self):
        if self._personal_addresses is None:
            from onchainpay_sdk.domains.personal_addresses import PersonalAddresses
            self._personal_addresses = PersonalAddresses(self, self._base_url)

        return self._personal_addresses

    @property
    def orders(self):
        if self._orders is None:
            from onchainpay_sdk.domains.orders import Orders
            self._orders = Orders(self, self._base_url)

        return self._orders

    @property
    def withdraws(self):
        if self._withdraws is None:
            from onchainpay_sdk.domains.withdraws import Withdraws
            self._withdraws = Withdraws(self, self._base_url)

        return self._withdraws

    @property
    def crosschain_bridge(self):
        if self._crosschain_bridge is None:
            from onchainpay_sdk.domains.crosschain_bridge import CrosschainBridge
            self._crosschain_bridge = CrosschainBridge(self, self._base_url)

        return self._crosschain_bridge

    @property
    def crosschain_swaps(self):
        if self._crosschain_swaps is None:
            from onchainpay_sdk.domains.crosschain_swaps import CrosschainSwaps
            self._crosschain_swaps = CrosschainSwaps(self, self._base_url)

        return self._crosschain_swaps

    @property
    def auto_swaps(self):
        if self._auto_swaps is None:
            from onchainpay_sdk.domains.auto_swaps import AutoSwaps
            self._auto_swaps = AutoSwaps(self, self._base_url)

        return self._auto_swaps

    @property
    def basic_actions(self):
        if self._basic_actions is None:
            from onchainpay_sdk.domains.basic_actions import BasicActions
            self._basic_actions = BasicActions(self, self._base_url)

        return self._basic_actions

    @property
    def recurring_payments(self):
        if self._recurring_payments is None:
            from onchainpay_sdk.domains.recurring_payments import RecurringPayments
            self._recurring_payments = RecurringPayments(self, self._base_url)

        return self._recurring_payments

    @property
    def kyt(self):
        if self._kyt is None:
            from onchainpay_sdk.domains.kyt import KYT
            self._kyt = KYT(self, self._base_url)

        return self._kyt

    @property
    def partners_api(self):
        if self._partners_api is None:
            from onchainpay_sdk.domains.partners_api import PartnersApi
            self._partners_api = PartnersApi(self, self._partners_base_url)

        return self._partners_api

    @property
    def orphan_transactions(self):
        if self._orphan_transactions is None:
            from onchainpay_sdk.domains.orphan_transactions import OrphanTransactions
            self._orphan_transactions = OrphanTransactions(self, self._base_url)

        return self._orphan_transactions

    @property
    def address_book(self):
        if self._address_book is None:
            from onchainpay_sdk.domains.address_book import AddressBook
            self._address_book = AddressBook(self, self._base_url)

        return self._address_book

    @property
    def webhooks(self):
        if self._webhooks is None:
            from onchainpay_sdk.domains.webhooks import Webhooks
            self._webhooks = Webhooks(self, self._base_url)

        return self._webhooks
