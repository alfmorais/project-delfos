from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.api.schemas.data import (
    DataBulkPayload,
    DataMessageResponse,
    DataParams,
    DataPayload,
    DataResponse,
    DataResponseOptional,
    ListDataResponse,
)


def test_data_bulk_payload_success():
    payload = DataBulkPayload(start_day=datetime.now(), duration=5)

    assert payload.start_day
    assert payload.duration == 5


def test_data_bulk_payload_error():
    with pytest.raises(ValidationError) as error:
        DataBulkPayload(start_day="invalid date", duration=5)

    assert error.typename == "ValidationError"
    assert issubclass(error.type, ValidationError)


def test_data_message_response_success():
    response = DataMessageResponse(message="Success")

    assert response.message == "Success"


def test_data_message_response_error():
    with pytest.raises(ValidationError) as error:
        DataMessageResponse(message=12345)

    assert error.typename == "ValidationError"
    assert issubclass(error.type, ValidationError)


def test_data_params_success():
    params = DataParams(
        start_time=1627898400,
        end_time=1627984800,
        columns=["id", "timestamp"],
    )

    assert params.start_time == 1627898400
    assert params.end_time == 1627984800
    assert params.columns == ["id", "timestamp"]


def test_data_params_error():
    with pytest.raises(ValidationError) as error:
        DataParams(
            start_time=1627898400,
            end_time=1627984800,
            columns=["invalid_column"],
        )

    assert error.typename == "ValidationError"
    assert issubclass(error.type, ValidationError)


def test_data_payload_success():
    payload = DataPayload(
        timestamp=1627898400,
        wind_speed=Decimal("5.5"),
        power=Decimal("100.5"),
        ambient_temperature=Decimal("25.3"),
    )

    assert payload.timestamp == 1627898400
    assert payload.wind_speed == Decimal("5.5")
    assert payload.power == Decimal("100.5")
    assert payload.ambient_temperature == Decimal("25.3")


def test_data_payload_error():
    with pytest.raises(ValidationError) as error:
        DataPayload(
            timestamp="invalid timestamp",
            wind_speed="invalid decimal",
            power="invalid decimal",
            ambient_temperature="invalid decimal",
        )

    assert error.typename == "ValidationError"
    assert issubclass(error.type, ValidationError)


def test_data_response_success():
    response = DataResponse(
        id=1,
        timestamp=1627898400,
        wind_speed=Decimal("5.5"),
        power=Decimal("100.5"),
        ambient_temperature=Decimal("25.3"),
    )

    assert response.id == 1
    assert response.timestamp == 1627898400
    assert response.wind_speed == Decimal("5.5")
    assert response.power == Decimal("100.5")
    assert response.ambient_temperature == Decimal("25.3")


def test_data_response_error():
    with pytest.raises(ValidationError) as error:
        DataResponse(
            id="invalid id",
            timestamp="invalid timestamp",
            wind_speed="invalid decimal",
            power="invalid decimal",
            ambient_temperature="invalid decimal",
        )

    assert error.typename == "ValidationError"
    assert issubclass(error.type, ValidationError)


def test_list_data_response_success():
    response = ListDataResponse(
        response=[
            DataResponseOptional(
                id=1,
                timestamp=1627898400,
                wind_speed=Decimal("5.5"),
                power=Decimal("100.5"),
                ambient_temperature=Decimal("25.3"),
            ),
            DataResponseOptional(
                id=2,
                timestamp=1627898500,
                wind_speed=Decimal("6.0"),
                power=Decimal("101.0"),
                ambient_temperature=Decimal("26.0"),
            ),
        ]
    )

    assert len(response.response) == 2
    assert response.response[0].id == 1
    assert response.response[1].id == 2


def test_list_data_response_error():
    with pytest.raises(ValidationError) as error:
        ListDataResponse(
            response=[
                {
                    "id": "invalid id",
                    "timestamp": "invalid timestamp",
                    "wind_speed": "invalid decimal",
                    "power": "invalid decimal",
                    "ambient_temperature": "invalid decimal",
                }
            ]
        )

    assert error.typename == "ValidationError"
    assert issubclass(error.type, ValidationError)
