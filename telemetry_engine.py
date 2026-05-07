import logging
import random
import time
from datetime import datetime, timezone
from enum import Enum
from typing import Dict

from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] ESG_Oracle: %(message)s")
logger = logging.getLogger("CarbonOracle")


class GridStatus(str, Enum):
    GREEN = "GREEN"
    AMBER = "AMBER"
    RED = "RED"


class CarbonData(BaseModel):
    timestamp: str
    region: str
    intensity_gco2_kwh: int
    grid_status: GridStatus


class CarbonIntensityAPI:
    """Simulates real-time grid carbon intensity with a 5-minute TTL cache."""

    SUPPORTED_REGIONS = frozenset({"DE", "FR", "IE", "UK", "NL"})
    TTL_SECONDS = 300

    def __init__(self):
        self._cache: Dict[str, tuple[float, CarbonData]] = {}

    def get_live_carbon_intensity(self, region: str) -> CarbonData:
        region = region.upper()

        if region not in self.SUPPORTED_REGIONS:
            logger.error(f"Rejected request: Region '{region}' is out of bounds.")
            raise ValueError(f"Region '{region}' is not supported.")

        current_time = time.time()

        if region in self._cache:
            expires_at, cached_data = self._cache[region]
            if current_time < expires_at:
                logger.info(f"Serving CACHED carbon data for {region}")
                return cached_data

        intensity_models = {
            "FR": random.randint(30, 60),
            "UK": random.randint(150, 250),
            "IE": random.randint(100, 300),
            "NL": random.randint(200, 400),
            "DE": random.randint(300, 500)
        }

        intensity = intensity_models.get(region, 250)
        status = GridStatus.GREEN if intensity < 150 else GridStatus.AMBER if intensity < 350 else GridStatus.RED

        logger.info(f"Fetched NEW Carbon Intensity for {region}: {intensity} gCO2eq/kWh [{status.value}]")

        response_data = CarbonData(
            timestamp=datetime.now(timezone.utc).isoformat(),
            region=region,
            intensity_gco2_kwh=intensity,
            grid_status=status
        )

        self._cache[region] = (current_time + self.TTL_SECONDS, response_data)
        return response_data