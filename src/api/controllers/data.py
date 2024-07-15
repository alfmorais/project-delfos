import random
from datetime import timedelta
from http import HTTPStatus
from typing import Dict, List

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.api.models import Data
from src.api.schemas import DataBulkPayload, DataParams, DataPayload


class DataController:
    def __init__(self, data: Data = Data) -> None:
        self.model = data

    def create(self, data: DataPayload, session: Session) -> Data:
        new_data = self.model(
            timestamp=data.timestamp,
            wind_speed=data.wind_speed,
            power=data.power,
            ambient_temperature=data.ambient_temperature,
        )
        session.add(new_data)
        session.commit()
        session.refresh(new_data)
        return new_data

    def retrieve(self, id: int, session: Session) -> Data:
        data = session.scalar(select(self.model).where(self.model.id == id))

        if data:
            return data

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Data com o ID {id} não encontrado",
        )

    def read(self, params: DataParams, session: Session) -> List[Data]:
        query = (
            session.query(self.model)
            .filter(
                and_(
                    self.model.timestamp >= params.start_time,
                    self.model.timestamp <= params.end_time,
                )
            )
            .all()
        )

        response = {
            "response": [
                {
                    "id": data.id,
                    "timestamp": data.timestamp,
                    "wind_speed": data.wind_speed,
                    "power": data.power,
                    "ambient_temperature": data.ambient_temperature,
                }
                for data in query
            ]
        }
        return response

    def delete(self, id: int, session: Session) -> Dict:
        data = session.scalar(select(self.model).where((self.model.id == id)))

        if data:
            session.delete(data)
            session.commit()
            return {"message": "Data deletado do Banco de Dados"}

        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Data com o ID {id} não encontrado",
        )

    def bulk(self, data: DataBulkPayload, session: Session) -> Dict:
        data_bulk_objects = list()

        start_time = data.start_day
        end_time = start_time + timedelta(days=data.duration)
        current_time = start_time

        while current_time <= end_time:
            payload = self.model(
                timestamp=int(current_time.timestamp()),
                wind_speed=random.uniform(0.0, 50.0),
                power=random.uniform(0.0, 1000.0),
                ambient_temperature=random.uniform(10.0, 35.0),
            )
            data_bulk_objects.append(payload)
            current_time += timedelta(minutes=1)

        try:
            session.bulk_save_objects(data_bulk_objects)
            session.commit()

            quantity = len(data_bulk_objects)

            return {"message": f"{quantity} objects inserted successfully"}

        except Exception as error:
            session.rollback()

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=str(error),
            )


data_controller = DataController()
