import secrets
import uuid

from api.dependencies.database import async_session
from api.crud.application import db_create_application
from api.schemas.core.application import ApplicatitonInDBSchema, ApplicationRole
from api.utils.hash import hash_password

async def create_admin_application():
    db = async_session()

    # Create the admin application
    client_id = str(uuid.uuid4())
    client_secret = secrets.token_urlsafe(24)
    admin_application = ApplicatitonInDBSchema(
        client_id=client_id,
        hashed_client_secret=hash_password(client_secret),
        role=ApplicationRole.admin
    )
    db_application = await db_create_application(db, admin_application)

    print(f'Admin client_id: {client_id}')
    print(f'Admin client_secret: {client_secret}')

    await db.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_admin_application())
