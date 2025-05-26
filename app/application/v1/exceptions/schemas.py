from pydantic import BaseModel, Field


class ErrorResponseSchema(BaseModel):
    """Schema for error responses.

    This schema is used to format error responses in a consistent way across the application.
    It includes the error message and any additional details about the error.

    Attributes:
        error: A descriptive message explaining what went wrong
    """

    error: str = Field(..., description='Error message describing what went wrong')


class ValidationErrorResponseSchema(ErrorResponseSchema):
    """Schema for validation error responses.

    This schema extends the base error response with validation-specific error information.

    Attributes:
        error: A descriptive message explaining what went wrong with the validation
        field: The field that failed validation (if applicable)
    """

    field: str | None = Field(None, description='The field that failed validation')


class NameErrorResponseSchema(ErrorResponseSchema):
    """Schema for name-related error responses.

    This schema extends the base error response with name-specific error information.

    Attributes:
        error: A descriptive message explaining what went wrong with the name
        name: The name that caused the error (if applicable)
    """

    name: str | None = Field(None, description='The name that caused the error')


class CountryErrorResponseSchema(ErrorResponseSchema):
    """Schema for country-related error responses.

    This schema extends the base error response with country-specific error information.

    Attributes:
        error: A descriptive message explaining what went wrong with the country
        country_code: The country code that caused the error (if applicable)
    """

    country_code: str | None = Field(
        None, description='The country code that caused the error'
    )
