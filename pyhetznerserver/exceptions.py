class HetznerAPIError(Exception):
    def __init__(self, message: str, status_code: int = None, error_code: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code

class AuthenticationError(HetznerAPIError):
    pass

class ValidationError(HetznerAPIError):
    pass

class ServerNotFoundError(HetznerAPIError):
    pass

class RateLimitError(HetznerAPIError):
    pass

class ConflictError(HetznerAPIError):
    pass

class ResourceLimitError(HetznerAPIError):
    pass

class ActionFailedError(HetznerAPIError):
    pass 