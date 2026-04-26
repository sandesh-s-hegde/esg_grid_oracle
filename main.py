import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from telemetry_engine import CarbonIntensityAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] ESG_API: %(message)s")
logger = logging.getLogger("FastAPI")

app = FastAPI(
    title="ESG Grid Oracle API",
    description="Real-time Carbon Telemetry for Autonomous Supply Chain Routing",
    version="1.0.0"
)

oracle = CarbonIntensityAPI()


class CarbonResponse(BaseModel):
    timestamp: str
    region: str
    intensity_gco2_kwh: int
    grid_status: str


@app.get("/health")
def health_check():
    return {"status": "online", "service": "ESG Grid Oracle"}


@app.get("/api/v1/carbon/{region}", response_model=CarbonResponse)
def get_carbon_intensity(region: str):
    region = region.upper()
    if region not in oracle.supported_regions:
        logger.warning(f"Invalid region requested: {region}")
        raise HTTPException(
            status_code=400,
            detail=f"Region {region} not supported. Valid regions: {list(oracle.supported_regions)}"
        )

    return oracle.get_live_carbon_intensity(region)