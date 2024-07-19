from datetime import datetime
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from src.api.controllers.data import data_controller
from src.api.models import Data
from src.api.schemas import DataBulkPayload, DataParams, DataPayload


@patch("src.api.controllers.data.Session")
def test_create(mock_session):
    mock_session_instance = MagicMock()
    mock_session.return_value = mock_session_instance

    data_payload = DataPayload(
        timestamp=1234567890,
        wind_speed=10.0,
        power=100.0,
        ambient_temperature=20.0,
    )

    data = data_controller.create(data_payload, mock_session_instance)

    assert data.timestamp == data_payload.timestamp
    assert data.wind_speed == data_payload.wind_speed
    assert data.power == data_payload.power
    assert data.ambient_temperature == data_payload.ambient_temperature

    mock_session_instance.add.assert_called_once_with(data)
    mock_session_instance.commit.assert_called_once()
    mock_session_instance.refresh.assert_called_once_with(data)


@patch("src.api.controllers.data.Session")
def test_retrieve_success(mock_session):
    mock_session_instance = MagicMock()
    mock_session.return_value = mock_session_instance

    data = Data(
        id=1,
        timestamp=1234567890,
        wind_speed=10.0,
        power=100.0,
        ambient_temperature=20.0,
    )
    mock_session_instance.scalar.return_value = data
    result = data_controller.retrieve(1, mock_session_instance)

    assert result == data
    mock_session_instance.scalar.assert_called_once()


@patch("src.api.controllers.data.Session")
def test_retrieve_not_found(mock_session):
    mock_session_instance = MagicMock()
    mock_session.return_value = mock_session_instance
    mock_session_instance.scalar.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        data_controller.retrieve(1, mock_session_instance)

    assert excinfo.value.status_code == HTTPStatus.BAD_REQUEST
    assert str(excinfo.value.detail) == "Data com o ID 1 não encontrado"
    mock_session_instance.scalar.assert_called_once()


@patch("src.api.controllers.data.Session")
def test_read(mock_session):
    mock_session_instance = MagicMock()
    mock_session.return_value = mock_session_instance

    params = DataParams(
        columns="timestamp,wind_speed",
        start_time=1234567890,
        end_time=1234567990,
    )

    mock_data = [(1234567890, 10.0), (1234567900, 20.0)]
    mock_session_instance.execute.return_value.all.return_value = mock_data

    result = data_controller.read(params, mock_session_instance)

    expected_result = [
        {"timestamp": 1234567890, "wind_speed": 10.0},
        {"timestamp": 1234567900, "wind_speed": 20.0},
    ]

    assert result == expected_result
    mock_session_instance.execute.assert_called_once()


@patch("src.api.controllers.data.Session")
def test_delete_success(mock_session):
    mock_session_instance = MagicMock()
    mock_session.return_value = mock_session_instance

    data = Data(
        id=1,
        timestamp=1234567890,
        wind_speed=10.0,
        power=100.0,
        ambient_temperature=20.0,
    )
    mock_session_instance.scalar.return_value = data

    result = data_controller.delete(1, mock_session_instance)

    assert result == {"message": "Data deletado do Banco de Dados"}
    mock_session_instance.delete.assert_called_once_with(data)
    mock_session_instance.commit.assert_called_once()


@patch("src.api.controllers.data.Session")
def test_delete_not_found(mock_session):
    mock_session_instance = MagicMock()
    mock_session.return_value = mock_session_instance
    mock_session_instance.scalar.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        data_controller.delete(1, mock_session_instance)

    assert excinfo.value.status_code == HTTPStatus.BAD_REQUEST
    assert str(excinfo.value.detail) == "Data com o ID 1 não encontrado"
    mock_session_instance.scalar.assert_called_once()


@patch("src.api.controllers.data.Session")
def test_bulk_success(mock_session):
    mock_session_instance = MagicMock()
    mock_session.return_value = mock_session_instance

    data_payload = DataBulkPayload(
        start_day=datetime(2024, 7, 19),
        duration=1,
    )

    result = data_controller.bulk(data_payload, mock_session_instance)

    assert result["message"].startswith("1441 objetos inserido com sucesso")
    mock_session_instance.bulk_save_objects.assert_called_once()
    mock_session_instance.commit.assert_called_once()


@patch("src.api.controllers.data.Session")
def test_bulk_raises_http_exception(mock_session):
    mock_session_instance = MagicMock()
    mock_session.return_value = mock_session_instance

    data_payload = DataBulkPayload(
        start_day=datetime(2024, 7, 19),
        duration=1,
    )

    mock_session_instance.bulk_save_objects.side_effect = Exception(
        "Erro ao salvar objetos"
    )

    with pytest.raises(HTTPException) as excinfo:
        data_controller.bulk(data_payload, mock_session_instance)

    assert excinfo.value.status_code == HTTPStatus.BAD_REQUEST
    assert str(excinfo.value.detail) == "Erro ao salvar objetos"
    mock_session_instance.rollback.assert_called_once()
    mock_session_instance.commit.assert_not_called()
