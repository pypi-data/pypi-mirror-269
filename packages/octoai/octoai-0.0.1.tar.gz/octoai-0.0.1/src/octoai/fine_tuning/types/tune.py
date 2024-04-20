# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1
from .tune_details import TuneDetails
from .tune_result import TuneResult
from .tune_status import TuneStatus
from .tune_type import TuneType


class Tune(pydantic_v1.BaseModel):
    """
    A tune base class.
    """

    created_at: dt.datetime = pydantic_v1.Field()
    """
    The time this tune task was created.
    """

    deleted_at: typing.Optional[dt.datetime] = None
    description: str = pydantic_v1.Field()
    """
    The description of the tune.
    """

    details: TuneDetails = pydantic_v1.Field()
    """
    Tune details.
    """

    id: str = pydantic_v1.Field()
    """
    The ID of the LoRA tune.
    """

    name: str = pydantic_v1.Field()
    """
    The name of the tune.
    """

    output_lora_ids: typing.List[str] = pydantic_v1.Field()
    """
    The output LoRA IDs, if the task was successful.
    """

    result: typing.Optional[TuneResult] = None
    status: TuneStatus = pydantic_v1.Field()
    """
    The status of the associated task.
    """

    status_details: str = pydantic_v1.Field()
    """
    The details of the status, only used when the associated task failed.
    """

    succeeded_at: typing.Optional[dt.datetime] = None
    tenant_id: str = pydantic_v1.Field()
    """
    The tenant who requested the LoRA tune.
    """

    tune_type: TuneType = pydantic_v1.Field()
    """
    The type of this tune.
    """

    updated_at: dt.datetime = pydantic_v1.Field()
    """
    The time this tune task was updated.
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
