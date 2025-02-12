import enum
from fastapi import HTTPException, status


class ErrorTypeEnum(str, enum.Enum):
    # API errors cover any other type of problem
    # (e.g., a temporary problem with Tinyshop's servers),
    # and are extremely uncommon.
    API_ERROR = "api_error"
    # Invalid request errors arise when your request has invalid parameters.
    INVALID_REQUEST_ERROR = "invalid_request_error"


class StatusCodeEnum(int, enum.Enum):
    # Everything worked as expected.
    OK = status.HTTP_200_OK
    # The request was unacceptable, often due to missing a required parameter.
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    # No valid API key provided.
    UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
    # The parameters were valid but the request failed.
    REQUEST_FAILED = status.HTTP_402_PAYMENT_REQUIRED
    # The API key doesn’t have permissions to perform the request.
    FORBIDDEN = status.HTTP_403_FORBIDDEN
    # The requested resource doesn’t exist.
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    # The request conflicts with another request
    # (perhaps due to using the same idempotent key).
    CONFLICT = status.HTTP_409_CONFLICT
    # Too many requests hit the API too quickly.
    # We recommend an exponential backoff of your requests.
    TOO_MANY_REQUESTS = status.HTTP_429_TOO_MANY_REQUESTS


class TinyshopException(HTTPException):
    def __init__(
        self,
        status_code: StatusCodeEnum,
        error_type: ErrorTypeEnum,
        code: str = None,
        message: str = None,
        param: str = None,
    ):
        super().__init__(status_code=status_code, detail=message)
        self.type = error_type
        # CRUD validation failed code - specific for each model
        # Reference - https://docs.stripe.com/error-codes
        self.code = code
        self.message = message
        self.param = param
