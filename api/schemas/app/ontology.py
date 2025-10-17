from pydantic import BaseModel


class OntologyRequestParams(BaseModel):
    env: str
