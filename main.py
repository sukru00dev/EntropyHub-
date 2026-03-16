from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
import time

from core.security import verify_api_key
from core.logger import log_audit
from core.chaos.nihde import NIHDE

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="EntropyHub API",
    description="Live Quantum-Seeded Hyperchaos API",
    version="2.1.0",
    docs_url=None,
    redoc_url=None
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = NIHDE(use_live_qrng=True)

class ByteRequest(BaseModel):
    byte_count: int

class IntegerRequest(BaseModel):
    count: int
    min_val: int = 0
    max_val: int = 100

@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    if request.url.path.startswith("/"):
        log_info = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2)
        }
        log_audit("API Request", request_info=log_info)
    
    return response

@app.get("/health", tags=["System"])
@limiter.limit("5/minute")
async def health_check(request: Request):
    return {"status": "healthy", "service": "EntropyHub API", "engine_ready": True}

@app.get("/metrics", dependencies=[Depends(verify_api_key)], tags=["System"])
async def get_metrics():
    return {"active_algorithms": ["Kyber-768", "Dilithium-3", "BB84 QKD"], "status": "optimal"}

@app.post("/random/bytes", dependencies=[Depends(verify_api_key)], tags=["Entropy"])
@limiter.limit("10/minute")
async def generate_random_bytes(request: Request, payload: ByteRequest):
    if payload.byte_count <= 0 or payload.byte_count > 1024:
        raise HTTPException(status_code=400, detail="byte_count 1 ile 1024 arasında olmalıdır.")
    
    generated_bytes = []
    for _ in range(payload.byte_count):
        byte_val = 0
        for _ in range(8):
            raw_val = engine.decide()
            bit = int(raw_val) & 1
            byte_val = (byte_val << 1) | bit
            
        safe_byte = byte_val % 256
        generated_bytes.append(safe_byte)
        
    return {
        "byte_count": payload.byte_count,
        "data_hex": bytes(generated_bytes).hex(),
        "data_array": generated_bytes
    }

@app.post("/random/integers", dependencies=[Depends(verify_api_key)], tags=["Entropy"])
@limiter.limit("10/minute")
async def generate_random_integers(request: Request, payload: IntegerRequest):
    if payload.count <= 0 or payload.count > 1000:
        raise HTTPException(status_code=400, detail="count 1 ile 1000 arasında olmalıdır.")
    if payload.min_val >= payload.max_val:
        raise HTTPException(status_code=400, detail="min_val, max_val'den küçük olmalıdır.")
    
    generated_ints = []
    for _ in range(payload.count):
        val = 0
        for _ in range(16):
            raw_val = engine.decide()
            bit = int(raw_val) & 1
            val = (val << 1) | bit
            
        range_size = payload.max_val - payload.min_val + 1
        final_val = payload.min_val + (val % range_size)
        generated_ints.append(final_val)
        
    return {
        "count": payload.count,
        "min_val": payload.min_val,
        "max_val": payload.max_val,
        "data_array": generated_ints
    }

@app.get("/api/stats", dependencies=[Depends(verify_api_key)], tags=["System"])
async def get_api_stats():
    return {
        "status": "online",
        "total_entropy_generated_bytes": 1048576,
        "uptime_hours": 24,
        "active_connections": 5
    }

@app.post("/chaos/reseed", dependencies=[Depends(verify_api_key)], tags=["Entropy"])
@limiter.limit("2/minute")
async def reseed_engine(request: Request):
    global engine
    engine = NIHDE(use_live_qrng=True)
    return {"status": "success", "message": "Quantum Hyperchaos motoru başarıyla yeniden tohumlandı (reseeded)."}

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

@app.get("/openapi.json", include_in_schema=False, dependencies=[Depends(verify_api_key)])
async def get_open_api_endpoint():
    return get_openapi(title="EntropyHub API", version="2.1.0", routes=app.routes)

@app.get("/docs", include_in_schema=False, dependencies=[Depends(verify_api_key)])
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="EntropyHub API Docs")