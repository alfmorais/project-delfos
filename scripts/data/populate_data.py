import json
import random
from datetime import datetime, timedelta

import httpx


class PopulateDateCommom:
    def __init__(self) -> None:
        self.data_information = list()
        self.start_time = datetime(2024, 6, 8)
        self.end_time = self.start_time + timedelta(days=10)

    def create_registries(self) -> None:
        raise NotImplementedError


class PopulateDateScript(PopulateDateCommom):
    def create_registries(self) -> None:
        current_time = self.start_time

        while current_time <= self.end_time:
            payload = json.dumps({
                "timestamp": int(current_time.timestamp()),
                "wind_speed": random.uniform(0.0, 50.0),
                "power": random.uniform(0.0, 1000.0),
                "ambient_temperature": random.uniform(10.0, 35.0),
            })
            self.data_information.append(payload)

            httpx.post(url="http://localhost:8000/v1/data", data=payload)

            current_time += timedelta(minutes=1)


if __name__ == "__main__":
    populate = PopulateDateScript()
    populate.create_registries()
