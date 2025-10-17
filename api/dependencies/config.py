import os

from pydantic_settings import BaseSettings
from sqlalchemy import URL

from api import __version__


class DataBaseSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        url_object = URL.create(
            drivername='postgresql+asyncpg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.DATABASE_NAME
        )
        url_object = url_object.update_query_dict({'ssl': 'require'})
        return url_object


class Settings(DataBaseSettings):
    # Application settings
    APP_NAME: str = 'DigiChecks Ontology Service'
    APP_VERSION: str = __version__

    # JWT settings
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_SECRET_KEY: str

    # LACES settings
    LACES_USERNAME: str
    LACES_PASSWORD: str


def get_settings():
    if '.env' in os.listdir():
        return Settings(_env_file='.env')
    elif 'BUILD_BUILDID' in os.environ:
        # Running in Azure DevOps pipeline so only need the db 
        # settings for migrations
        return DataBaseSettings()
    else:
        return Settings() 

settings = get_settings()
