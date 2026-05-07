import os
import secrets
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

load_dotenv()

API_KEY_NAME = "X-ESG-API-KEY"
EXPECTED_API_KEY = os.getenv("ESG_API_KEY", "dev-secret-key")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """Validates the incoming API key against timing attacks."""

    if not api_key or not secrets.compare_digest(api_key, EXPECTED_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing ESG API Key"
        )

    return api_key