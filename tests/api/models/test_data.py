from decimal import Decimal

import pytest
from sqlalchemy.exc import DataError, IntegrityError

from src.api.models import Data
from tests.factories import DataFactory


def test_insert_valid_data(session):
    data = DataFactory(
        timestamp=1625097600,
        wind_speed=Decimal("5.67"),
        power=Decimal("123.45"),
        ambient_temperature=Decimal("22.5"),
    )
    session.add(data)
    session.commit()

    assert data.id is not None
    assert isinstance(data.id, int)
    assert str(data) == f"Data[id={data.id}, timestamp={data.timestamp}]"

    session.delete(data)
    session.commit()


def test_insert_duplicate_id(session):
    first_data = DataFactory(
        id=1,
        timestamp=1625097600,
        wind_speed=Decimal("5.67"),
        power=Decimal("123.45"),
        ambient_temperature=Decimal("22.5"),
    )
    second_data = DataFactory(
        id=1,
        timestamp=1625097601,
        wind_speed=Decimal("6.67"),
        power=Decimal("124.45"),
        ambient_temperature=Decimal("23.5"),
    )
    session.add(first_data)
    session.commit()

    session.add(second_data)

    with pytest.raises(IntegrityError) as error:
        session.commit()

    session.rollback()

    assert error.typename == "IntegrityError"
    assert issubclass(error.type, IntegrityError)

    session.delete(first_data)
    session.commit()


@pytest.mark.parametrize(
    ("data", "expected_exception", "expected_description_exception"),
    [
        (
            Data(
                wind_speed=Decimal("5.67"),
                power=Decimal("123.45"),
                ambient_temperature=Decimal("22.5"),
            ),
            IntegrityError,
            "IntegrityError",
        ),
        (
            Data(
                timestamp=1625097600,
                power=Decimal("123.45"),
                ambient_temperature=Decimal("22.5"),
            ),
            IntegrityError,
            "IntegrityError",
        ),
        (
            Data(
                timestamp=1625097600,
                wind_speed="invalid_decimal",
                power=Decimal("123.45"),
                ambient_temperature=Decimal("22.5"),
            ),
            DataError,
            "DataError",
        ),
    ],
)
def test_data_integrity_error(
    session,
    data,
    expected_exception,
    expected_description_exception,
):
    session.add(data)

    with pytest.raises(expected_exception) as error:
        session.commit()

    assert error.typename == expected_description_exception
    assert issubclass(error.type, expected_exception)

    session.rollback()
