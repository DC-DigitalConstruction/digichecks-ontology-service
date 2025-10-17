# DigiChecks Ontology Service

The DigiChecks Ontology Service is part of the DigiChecks framework. This service is an intermediary between the BPM Engine and the permit ontology stored in the LACES platform. It provides the BPM Engine with standardised REST API endpoints so that the BPM is able to communicate with the ontology. This is done by implementing predefined SPARQL queries. The tool was developed within the DigiChecks project.

## Prerequisites

- Python 3.12.3
- PostgreSQL database
- uv (Python package manager)

## Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd digichecks-ontology-service
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Run database migrations**
   ```bash
   uv run alembic upgrade head
   ```

5. **Initialize database with admin application**
   ```bash
   uv run python init_database.py
   ```

   Save the generated `client_id` and `client_secret` for authentication.

6. **Start the development server**
   ```bash
   uv run uvicorn api.main:app --reload
   ```

The API will be available at `http://localhost:8000`. API documentation is accessible at `http://localhost:8000/docs`.

## Architecture

The service uses a FastAPI-based architecture with:
- **Authentication**: OAuth2 with JWT tokens, role-based access control (admin/user roles)
- **Database**: PostgreSQL with async SQLAlchemy and Alembic migrations
- **External Integration**: SPARQL queries to LACES ontology hub for permit data retrieval

Supported permit types:
- GCN (Great Crested Newt) permits
- Bat permits
- Power permits
- Building permits
- Austrian building permits

> Note that the permits must be mapped in `api/utils/enums.py`

The ontology service queries permit shapes and document requirements using SHACL vocabulary patterns, returning structured data about required documents and compliance requirements for each permit type.

## References

- [www.digichecks.eu](https://digichecks.eu/)
- [CORDIS EU Database](https://cordis.europa.eu/project/id/101058541/results)

This Project has received Funding from the European Union´s Horizon Europe research and innovation programme - Project 101058541 — DigiChecks
