from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class ApplicationRole(str, Enum):
    admin = 'admin'
    user = 'user'


class ApplicatitonInSchema(BaseModel):
    role: ApplicationRole = ApplicationRole.user


class ApplicatitonInDBSchema(ApplicatitonInSchema):
    client_id: UUID
    hashed_client_secret: str


class ApplicationOutSchema(BaseModel):
    client_id: UUID
    client_secret: str

    class Config:
        from_attributes = True
