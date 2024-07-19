from typing import Dict

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.orm import Session

from src.api.controllers import data_controller
from src.api.schemas import (
    DataBulkPayload,
    DataMessageResponse,
    DataParams,
    DataPayload,
    DataResponse,
)
from src.infrastructure.database import get_session

router = APIRouter(tags=["Data"], prefix="/v1/data")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=DataResponse,
)
def create_data(data: DataPayload, session: Session = Depends(get_session)):
    return data_controller.create(data, session)


@router.post(
    "/bulk-data",
    status_code=status.HTTP_201_CREATED,
    response_model=DataMessageResponse,
)
def bulk_data(data: DataBulkPayload, session: Session = Depends(get_session)):
    return data_controller.bulk(data, session)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=DataResponse,
)
def retrieve_data(id: int, session: Session = Depends(get_session)):
    return data_controller.retrieve(id, session)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=Page[Dict],
)
def read_data(
    params: DataParams = Depends(),
    session: Session = Depends(get_session),
):
    disable_installed_extensions_check()
    return paginate(data_controller.read(params, session))


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=DataMessageResponse,
)
def delete_data(id: int, session: Session = Depends(get_session)):
    return data_controller.delete(id, session)
