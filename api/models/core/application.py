from sqlalchemy import Column, String, UUID
from sqlalchemy import Enum as SQLAlchemyEnum

from api.dependencies.database import APPLICATION_TABLE, BaseModel
from api.schemas.core.application import ApplicationRole


class Application(BaseModel):
    __tablename__ = APPLICATION_TABLE.table_name
    __table_args__ = {'schema': APPLICATION_TABLE.schema_name}
    __id_prefix__ = 'ap'

    # Columns
    client_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    hashed_client_secret = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(ApplicationRole), nullable=False)
