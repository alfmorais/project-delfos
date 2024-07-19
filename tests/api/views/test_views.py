import random
from datetime import datetime, timedelta
from http import HTTPStatus

from sqlalchemy import delete

from src.api.models import Data
from tests.factories import DataFactory


def test_create_data_success(client):
    payload = {
        "timestamp": 1622476800,
        "wind_speed": "12.34",
        "power": "45.67",
        "ambient_temperature": "23.45",
    }
    response = client.post("/v1/data", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["timestamp"] == payload["timestamp"]


def test_create_data_error(client):
    payload = {
        "timestamp": "invalid",
        "wind_speed": "12.34",
        "power": "45.67",
        "ambient_temperature": "23.45",
    }
    response = client.post("/v1/data", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_retrieve_data_success(client, data_instance):
    response = client.get(f"/v1/data/{data_instance.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == data_instance.id


def test_retrieve_data_error(client):
    response = client.get("/v1/data/9999")

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_data_success(client, session):
    data_bulk_objects = list()

    start_time = datetime.fromisoformat(
        "2024-07-19T16:11:43.947Z".replace("Z", "+00:00")
    )
    timestamp_start_time = int(start_time.timestamp())

    end_time = start_time + timedelta(days=5)
    timestamp_end_time = int(end_time.timestamp())

    current_time = start_time

    while current_time <= end_time:
        payload = DataFactory(
            timestamp=int(current_time.timestamp()),
            wind_speed=random.uniform(0.0, 50.0),
            power=random.uniform(0.0, 1000.0),
            ambient_temperature=random.uniform(10.0, 35.0),
        )
        data_bulk_objects.append(payload)
        current_time += timedelta(minutes=1)

    session.bulk_save_objects(data_bulk_objects)
    session.commit()

    response = client.get(
        f"/v1/data?start_time={timestamp_start_time}&end_time={timestamp_end_time}"
    )

    assert response.status_code == 200


def test_read_data_error(client):
    response = client.get("/v1/data", params={"invalid_param": "value"})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_delete_data_success(client, data_instance):
    response = client.delete(f"/v1/data/{data_instance.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Data deletado do Banco de Dados"


def test_delete_data_error(client):
    response = client.delete("/v1/data/9999")

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_bulk_data_success(client, session):
    session.execute(delete(Data))
    session.commit()

    payload = {"start_day": "2024-07-19T15:23:43.592Z", "duration": 1}
    response = client.post("/v1/data/bulk-data", json=payload)

    assert response.json() == {"message": "1441 objetos inserido com sucesso"}
    assert response.status_code == HTTPStatus.CREATED


def test_bulk_data_error(client):
    payload = {
        "start_time": "",
        "end_time": "",
        "columns": [],
    }
    response = client.post("/v1/data/bulk-data", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
