from fastapi import APIRouter, Depends, HTTPException, status, Security
import requests
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import user_level, get_db, settings
from api.schemas.app.ontology import OntologyRequestParams
from api.enums import PermitType


ontology_router = APIRouter()

def laces_sparql_request(env: str, query: str):
    headers = {
        "Content-Type": "application/sparql-query"
    }

    try:
        response = requests.post(
            f'https://hub.laces.tech/{env}/sparql',
            auth=(settings.LACES_USERNAME, settings.LACES_PASSWORD), 
            headers=headers, 
            data=query
        )
        return response.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error connecting to LACES: {e}'
        )


@ontology_router.post(
    name='Get the information about a permit',
    path='/{permit_type}',
    status_code=status.HTTP_200_OK,
    dependencies=[Security(user_level)]
)
async def get_permit_info(
    permit_type: str,
    ontology_request_params: OntologyRequestParams,
    db: AsyncSession = Depends(get_db),
):
    try:
        mapped_permit_type = PermitType.from_type(permit_type)
    except ValueError:
        valid_permit_types = ', '.join([permit_type.value for permit_type in PermitType])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(f'Permit type \'{permit_type}\' not found. Must be '
                    f'one of: {valid_permit_types}')
        )

    sparql = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    PREFIX checks: <http://data.digichecks.eu/def/>
    PREFIX company: <https://hub.laces.tech/digichecks/private/development/test-permit-and-docs/>
    PREFIX sml: <https://w3id.org/sml/def#>

    SELECT ?documentURI ?documentName ?RequirementURI ?RequirementText WHERE {{
        ?PermitShape sh:targetClass <{mapped_permit_type.uri}> .
        ?PermitShape sh:property ?PermitPropertyShape . 
        ?PermitPropertyShape sh:path checks:isRequestedBy .

        ?PermitPropertyShape sh:node/sh:property ?RequestProperties . 
        ?RequestProperties sh:path sml:hasPart . 
        ?RequestProperties sh:qualifiedValueShape ?valueShape . 
        ?valueShape sh:class ?documentURI . 
        ?documentURI skos:prefLabel ?documentName . 

        OPTIONAL {{ 
            ?RequirementURI checks:isExpressedAs ?PermitShape . 
            ?RequirementURI rdf:value ?RequirementText . 
        }}
    }}
    """
    resp = laces_sparql_request(
        env=ontology_request_params.env, 
        query=sparql
    )
    return resp
