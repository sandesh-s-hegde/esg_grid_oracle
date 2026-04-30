import time
import logging
from typing import List
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from telemetry_engine import CarbonIntensityAPI
from auth import verify_api_key

# Enterprise Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] ESG_API: %(message)s")
logger = logging.getLogger("FastAPI")

# API Initialization
app = FastAPI(title="ESG Grid Oracle API", version="1.3.0")

# Security: CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core Engine & Telemetry State
oracle = CarbonIntensityAPI()
BOOT_TIME = time.time()

# Data Models
class CarbonResponse(BaseModel):
    timestamp: str
    region: str
    intensity_gco2_kwh: int
    grid_status: str

class BatchCarbonRequest(BaseModel):
    regions: List[str]

# Performance Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Routes
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    """Redirect root pings to Swagger UI Documentation."""
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    uptime = time.time() - BOOT_TIME
    return {
        "status": "online",
        "service": "ESG Grid Oracle",
        "uptime_seconds": round(uptime, 2)
    }

@app.get("/api/v1/carbon/{region}", response_model=CarbonResponse)
def get_carbon_intensity(region: str, api_key: str = Depends(verify_api_key)):
    region = region.upper()
    if region not in oracle.supported_regions:
        logger.warning(f"Invalid region requested: {region}")
        raise HTTPException(status_code=400, detail=f"Region {region} not supported.")
    return oracle.get_live_carbon_intensity(region)

@app.post("/api/v1/carbon/batch", response_model=List[CarbonResponse])
def get_batch_carbon_intensity(request: BatchCarbonRequest, api_key: str = Depends(verify_api_key)):
    results = []
    for r in request.regions:
        r_upper = r.upper()
        if r_upper in oracle.supported_regions:
            results.append(oracle.get_live_carbon_intensity(r_upper))
    return results