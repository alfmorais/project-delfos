import random
from datetime import datetime
from decimal import Decimal

import factory

from src.api.models import Data


def generate_decimal_numbers() -> Decimal:
    number = random.uniform(0.0, 100.0)
    formated_number = round(Decimal(number), 2)
    return formated_number


def generate_timestamp() -> int:
    return int(datetime.now().timestamp())


class DataFactory(factory.Factory):
    class Meta:
        model = Data

    id = factory.Sequence(lambda n: n + 1)
    timestamp = factory.LazyFunction(lambda: generate_timestamp())
    wind_speed = factory.LazyFunction(lambda: generate_decimal_numbers())
    power = factory.LazyFunction(lambda: generate_decimal_numbers())
    ambient_temperature = factory.LazyFunction(
        lambda: generate_decimal_numbers(),
    )
