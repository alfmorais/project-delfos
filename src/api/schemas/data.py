from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


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


class DataResponseOptional(BaseModel):
    id: Optional[int]
    timestamp: Optional[int]
    wind_speed: Optional[Decimal]
    power: Optional[Decimal]
    ambient_temperature: Optional[Decimal]


class ListDataResponse(BaseModel):
    response: List[DataResponseOptional]


class DataMessageResponse(BaseModel):
    message: str


class DataParams(BaseModel):
    start_time: int
    end_time: int
    columns: Optional[List[str]] = Field(
        None,
        description="List of fields to return",
    )

    @field_validator("columns")
    def validate_columns(cls, columns):
        valid_columns = [
            "id",
            "timestamp",
            "wind_speed",
            "power",
            "ambient_temperature",
        ]
        for column in columns:
            if column not in valid_columns:
                raise ValueError(f"Coluna invalída: {column}")

        return columns
