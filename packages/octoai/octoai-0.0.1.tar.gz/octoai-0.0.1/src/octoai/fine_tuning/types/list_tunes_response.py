# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1
from .tune import Tune


class ListTunesResponse(pydantic_v1.BaseModel):
    """
    The list tunes response.
    """

    data: typing.List[Tune] = pydantic_v1.Field()
    """
    List of tunes.
    """

    has_more: bool = pydantic_v1.Field()
    """
    True if it has more items than the returned list.
    """

    total: int = pydantic_v1.Field()
    """
    Total number of tunes.
    """

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
