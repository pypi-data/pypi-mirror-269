class onchainpay_sdkError(Exception):
    def __init__(
            self,
            message: str,
    ):
        super(onchainpay_sdkError, self).__init__(message)


class AuthenticationError(onchainpay_sdkError):
    def __init__(self, message: str):
        super(AuthenticationError, self).__init__(message)


class InternalSDKError(onchainpay_sdkError):
    def __init__(self, message: str):
        super(InternalSDKError, self).__init__(message)
