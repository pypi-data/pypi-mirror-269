from __future__ import annotations


class CustomException(Exception):
    def __init__(
        self,
        custom_status_code: int | None = None,
        custom_error_code: str | None = None,
        custom_error_message: str | None = None,
        custom_error_details: str | None = None,
    ) -> None:
        if custom_status_code:
            self.STATUS_CODE = custom_status_code
        if custom_error_code:
            self.ERROR_CODE = custom_error_code
        if custom_error_message:
            self.ERROR_MESSAGE = custom_error_message
        if custom_error_details:
            self.ERROR_DETAILS = custom_error_details
        super().__init__(self.ERROR_MESSAGE)


class RequestValidationException(CustomException):
    STATUS_CODE = 422
    ERROR_CODE = "REQUEST_VALIDATION_EXCEPTION"
    ERROR_MESSAGE = "Request Validation Exception"
    ERROR_DETAILS = "Invalid request body"


class GenericException(CustomException):
    STATUS_CODE = 500
    ERROR_CODE = "GENERIC_EXCEPTION"
    ERROR_MESSAGE = "Generic Exception"


class PydanticBaseModelException(CustomException):
    STATUS_CODE = 500
    ERROR_CODE = "PYDANTIC_MODEL_EXCEPTION"
    ERROR_MESSAGE = "Model does not inherit Pydantic Base Model!"
