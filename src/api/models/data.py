from decimal import Decimal

from sqlalchemy import DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base


class Data(Base):
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    timestamp: Mapped[int] = mapped_column(Integer)
    wind_speed: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    power: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    ambient_temperature: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))

    def __repr__(self) -> str:
        return f"Data[id={self.id}, timestamp={self.timestamp}]"
