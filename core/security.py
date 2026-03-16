import os
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

VALID_API_KEYS = os.getenv("ENTROPYHUB_API_KEYS", "").split(",")
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

async def verify_api_key(api_key_header: str = Security(api_key_header)):
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key eksik (x-api-key header gerekli)",
        )
    if api_key_header not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Gecersiz API Key",
        )
    return api_key_header