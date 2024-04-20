# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1
from .error_response_validation_errors_value import ErrorResponseValidationErrorsValue


class ErrorResponse(pydantic_v1.BaseModel):
    """
    An OpenAI API compatible schema for a error response.
    """

    code: typing.Optional[str] = None
    message: str
    object: typing.Optional[str] = None
    param: typing.Optional[str] = None
    type: str
    validation_errors: typing.Optional[typing.Dict[str, typing.Optional[ErrorResponseValidationErrorsValue]]] = None

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
