from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.infrastructure.server.settings import settings

engine = create_engine(settings.SOURCE_DATABASE_URL)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
