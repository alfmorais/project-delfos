from unittest.mock import MagicMock, patch

from sqlalchemy.orm import DeclarativeBase

from src.infrastructure.database import Base, get_session


@patch("src.infrastructure.database.utils.session.Session")
@patch("src.infrastructure.database.utils.session.create_engine")
def test_get_session(mock_create_engine, mock_session):
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    mock_session_instance = MagicMock()
    mock_session.return_value.__enter__.return_value = mock_session_instance

    session_generator = get_session()
    session = next(session_generator)

    assert session == mock_session_instance

    session_generator.close()
    mock_session_instance.close.assert_called_once()


def test_base_class_for_models():
    assert issubclass(Base, DeclarativeBase)
