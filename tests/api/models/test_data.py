import pytest
from decimal import Decimal
from sqlalchemy.exc import IntegrityError, DataError
from src.api.models import Data


def test_insert_valid_data(session):
    data = Data(
        timestamp=1625097600,
        wind_speed=Decimal("5.67"),
        power=Decimal("123.45"),
        ambient_temperature=Decimal("22.5"),
    )
    session.add(data)
    session.commit()

    assert data.id is not None
    assert isinstance(data.id, int)

    session.delete(data)
    session.commit()


def test_insert_duplicate_id(session):
    first_data = Data(
        id=1,
        timestamp=1625097600,
        wind_speed=Decimal("5.67"),
        power=Decimal("123.45"),
        ambient_temperature=Decimal("22.5"),
    )
    second_data = Data(
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
    "data,expected_exception,description_exception",
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
def test_data_integrity(
    session,
    data,
    expected_exception,
    description_exception,
):
    session.add(data)

    with pytest.raises(expected_exception) as error:
        session.commit()

    assert error.typename == description_exception
    assert issubclass(error.type, expected_exception)

    session.rollback()
