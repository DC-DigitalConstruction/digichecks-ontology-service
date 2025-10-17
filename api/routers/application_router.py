import secrets
import uuid

from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.application import db_create_application
from api.dependencies import get_db, admin_level
from api.schemas import (
    ApplicatitonInSchema,
    ApplicatitonInDBSchema,
    ApplicationOutSchema
)
from api.utils.hash import hash_password


router = APIRouter()


@router.post(
    name='Create Application',
    path='',
    status_code=status.HTTP_201_CREATED,
    response_model=ApplicationOutSchema,
    dependencies=[Security(admin_level)]
)
async def create_application(
    application: ApplicatitonInSchema,
    requesting_application=Security(admin_level),
    db: AsyncSession = Depends(get_db)
):
    # Generate the client id and secret
    client_id = uuid.uuid4()
    client_secret = secrets.token_urlsafe(24)

    # Create the application schema for the database with
    # the hashed client secret
    application = ApplicatitonInDBSchema(
        client_id=client_id,
        hashed_client_secret=hash_password(client_secret)
    )

    db_application = await db_create_application(db, application)

    # Create the response
    resp = ApplicationOutSchema(
        client_id=db_application.client_id,
        client_secret=client_secret
    )

    return resp
