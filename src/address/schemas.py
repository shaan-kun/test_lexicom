from pydantic import BaseModel


class Address(BaseModel):
    phone: str
    address: str
