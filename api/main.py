from fastapi import FastAPI

from api.dependencies.config import settings
from api.routers.application_router import router as applications_router
from api.routers.auth_router import router as auth_router
from api.routers.ontology_router import ontology_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


tags_metadata = [
    {
        'name': 'Token', 
        'description': 'Retrieving a token'
    },
    {
        'name': 'Client Application', 
        'description': 'Requests to create an application'
    },
    {
        'name': 'Ontology', 
        'description': 'Requests to interact with the ontology'
    }
]

app.openapi_tags = tags_metadata

app.include_router(
    applications_router, prefix='/application', tags=['Client Application'])
app.include_router(
    ontology_router, prefix='/ontology', tags=['Ontology'])
app.include_router(
    auth_router, prefix='/auth', tags=['Token'])
