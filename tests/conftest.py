from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src.api import app
from src.infrastructure.database import Base, get_session
from tests.factories import DataFactory


@pytest.fixture(scope="module")
def client(session) -> Generator:
    def get_db_override():
        return session

    with TestClient(app) as app_client:
        app.dependency_overrides[get_session] = get_db_override

        yield app_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture(scope="module")
def session(engine) -> Generator:
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def data_instance(session):
    data = DataFactory()
    session.add(data)
    session.commit()
    session.refresh(data)
    return data
