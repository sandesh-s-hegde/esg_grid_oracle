import time
import logging
from typing import List
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel, Field
from telemetry_engine import CarbonIntensityAPI
from auth import verify_api_key

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] ESG_API: %(message)s")
logger = logging.getLogger("FastAPI")

app = FastAPI(title="ESG Grid Oracle API", version="1.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oracle = CarbonIntensityAPI()
BOOT_TIME = time.time()

class CarbonResponse(BaseModel):
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp of the reading")
    region: str = Field(..., description="2-letter country code", examples=["FR", "DE"])
    intensity_gco2_kwh: int = Field(..., description="Grams of CO2 equivalent per kWh")
    grid_status: str = Field(..., description="Dispatch status: GREEN, AMBER, or RED", examples=["GREEN"])

class BatchCarbonRequest(BaseModel):
    regions: List[str] = Field(..., description="List of 2-letter country codes to query", examples=[["FR", "DE", "IE"]])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled system crash on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal System Failure",
            "message": "The ESG Oracle encountered an unexpected fault.",
            "path": request.url.path
        }
    )

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

@app.get("/health", tags=["System"])
def health_check():
    uptime = time.time() - BOOT_TIME
    return {
        "status": "online",
        "service": "ESG Grid Oracle",
        "uptime_seconds": round(uptime, 2)
    }

@app.get("/api/v1/carbon/{region}", response_model=CarbonResponse, dependencies=[Depends(verify_api_key)], tags=["Telemetry"])
def get_carbon_intensity(region: str):
    region = region.upper()
    if region not in oracle.SUPPORTED_REGIONS:
        logger.warning(f"Invalid region requested: {region}")
        raise HTTPException(status_code=400, detail=f"Region {region} not supported.")
    return oracle.get_live_carbon_intensity(region)

@app.post("/api/v1/carbon/batch", response_model=List[CarbonResponse], dependencies=[Depends(verify_api_key)], tags=["Telemetry"])
def get_batch_carbon_intensity(request: BatchCarbonRequest):
    results = []
    for r in request.regions:
        r_upper = r.upper()
        if r_upper in oracle.SUPPORTED_REGIONS:
            results.append(oracle.get_live_carbon_intensity(r_upper))
    return results
