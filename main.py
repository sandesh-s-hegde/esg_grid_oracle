import logging
import time
from contextlib import asynccontextmanager
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field

from auth import verify_api_key
from telemetry_engine import CarbonIntensityAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] ESG_API: %(message)s")
logger = logging.getLogger("FastAPI")

app_state = {}
oracle = CarbonIntensityAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app_state["boot_time"] = time.time()
    logger.info("ESG Oracle booting sequence initiated.")
    yield
    logger.info("ESG Oracle shutting down safely.")

app = FastAPI(title="ESG Grid Oracle API", version="1.4.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CarbonResponse(BaseModel):
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp of the reading")
    region: str = Field(..., description="2-letter country code", examples=["FR", "DE"])
    intensity_gco2_kwh: int = Field(..., description="Grams of CO2 equivalent per kWh")
    grid_status: str = Field(..., description="Dispatch status: GREEN, AMBER, or RED", examples=["GREEN"])

class BatchCarbonRequest(BaseModel):
    regions: List[str] = Field(..., description="List of 2-letter country codes to query", examples=[["FR", "DE", "IE"]])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
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


@app.get("/", include_in_schema=False)
def root_redirect():
    """Redirects the root URL directly to the API documentation."""
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["System"])
def health_check() -> dict:
    """Returns the operational status and uptime of the service."""
    uptime = time.time() - app_state.get("boot_time", time.time())
    return {
        "status": "online",
        "service": "ESG Grid Oracle",
        "uptime_seconds": round(uptime, 2)
    }


secure_router = APIRouter(prefix="/api/v1/carbon", dependencies=[Depends(verify_api_key)])

@secure_router.get("/{region}", response_model=CarbonResponse, tags=["Telemetry"])
def get_carbon_intensity(region: str, response: Response):
    """Retrieves real-time carbon intensity data for a specific supported region."""
    region = region.upper()
    if region not in oracle.SUPPORTED_REGIONS:
        raise HTTPException(status_code=400, detail=f"Region '{region}' is not supported.")

    response.headers["Cache-Control"] = f"public, max-age={oracle.TTL_SECONDS}"
    return oracle.get_live_carbon_intensity(region)

@secure_router.post("/batch", response_model=List[CarbonResponse], tags=["Telemetry"])
def get_batch_carbon_intensity(request: BatchCarbonRequest):
    """Retrieves real-time carbon intensity data for multiple regions simultaneously."""
    results = []
    for r in request.regions:
        r_upper = r.upper()
        if r_upper in oracle.SUPPORTED_REGIONS:
            results.append(oracle.get_live_carbon_intensity(r_upper))
    return results

@secure_router.delete("/cache", tags=["Admin"])
def clear_oracle_cache() -> dict:
    """Admin override to manually flush the telemetry cache."""
    items_removed = oracle.purge_cache()
    return {"message": "Cache successfully purged", "items_removed": items_removed}

app.include_router(secure_router)