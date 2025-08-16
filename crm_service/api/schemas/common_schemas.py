from typing import Generic, TypeVar

from ninja.schema import Schema
from pydantic import Field


ResponseData = TypeVar("ResponseData")
description = "This is any collections data from api respopnse"


class ApiResponse(Schema, Generic[ResponseData]):
    data: ResponseData | dict = Field(
        default_factory=dict,
        description=description,
        examples=" {'key': 'value'}",
    )
    
