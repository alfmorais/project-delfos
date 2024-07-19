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


class DataMessageResponse(BaseModel):
    message: str


class DataParams(BaseModel):
    start_time: int
    end_time: int
    columns: str = Field(
        description="List of fields to return",
        default="id,timestamp,wind_speed,power,ambient_temperature",
        examples="id,timestamp,wind_speed,power,ambient_temperature",
    )

    @field_validator("columns")
    def validate_columns(cls, columns: str) -> List:
        valid_columns = [
            "id",
            "timestamp",
            "wind_speed",
            "power",
            "ambient_temperature",
        ]
        formated_columns = []

        for column in columns.split(","):
            if column not in valid_columns:
                raise ValueError(f"Coluna invalída: {column}")

            formated_columns.append(column)

        return formated_columns
