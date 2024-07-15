from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel


class DataPayload(BaseModel):
    timestamp: int
    wind_speed: Decimal
    power: Decimal
    ambient_temperature: Decimal


class DataBulkPayload(BaseModel):
    start_day: datetime
    duration: int


class DataResponse(DataPayload):
    id: int


class ListDataResponse(BaseModel):
    response: List[DataResponse]


class DataMessageResponse(BaseModel):
    message: str


class DataParams(BaseModel):
    start_time: int
    end_time: int
