from fastapi import APIRouter, Response, status, HTTPException

from .schemas import Address
from ..database import redis_object

router = APIRouter(prefix="/address", tags=["Address"])


@router.get("/{phone}/", summary='Получение адреса')
def get_address(phone: str) -> str:
    address = redis_object.get(phone)
    return address


@router.post(
    "/",
    summary='Создание адреса',
    status_code=status.HTTP_201_CREATED
)
def create_address(data: Address):
    address = redis_object.get(data.phone)
    if address:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Адрес для телефона {data.phone} уже существует!',
        )
    redis_object.set(data.phone, data.address)
    return Response(status_code=status.HTTP_201_CREATED)


@router.put("/", summary='Изменение адреса')
def update_address(data: Address):
    redis_object.set(data.phone, data.address)
