import secrets
from typing import Optional

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from config import settings

API_KEY_NAME = "X-ESG-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """Validates the incoming API key against timing attacks using Pydantic settings."""
    if not api_key or not secrets.compare_digest(api_key, settings.esg_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing ESG API Key"
        )

    return api_key