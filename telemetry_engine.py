import time
import random
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] ESG_Oracle: %(message)s")
logger = logging.getLogger("CarbonOracle")


class CarbonIntensityAPI:
    """Simulates real-time grid carbon intensity with a 5-minute TTL cache."""

    def __init__(self):
        self.supported_regions = {"DE", "FR", "IE", "UK", "NL"}
        self._cache = {}
        self.ttl_seconds = 300

    def get_live_carbon_intensity(self, region: str) -> dict:
        if region not in self.supported_regions:
            logger.error(f"Region {region} is out of bounds.")
            return {"error": "Region not supported"}

        current_time = time.time()

        if region in self._cache and (current_time - self._cache[region]['timestamp'] < self.ttl_seconds):
            logger.info(f"Serving CACHED carbon data for {region}")
            return self._cache[region]['data']

        intensity_models = {
            "FR": random.randint(30, 60),
            "UK": random.randint(150, 250),
            "IE": random.randint(100, 300),
            "NL": random.randint(200, 400),
            "DE": random.randint(300, 500)
        }

        intensity = intensity_models.get(region, 250)
        status = "GREEN" if intensity < 150 else "AMBER" if intensity < 350 else "RED"

        logger.info(f"Fetched NEW Carbon Intensity for {region}: {intensity} gCO2eq/kWh [{status}]")

        response_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "region": region,
            "intensity_gco2_kwh": intensity,
            "grid_status": status
        }

        self._cache[region] = {'timestamp': current_time, 'data': response_data}
        return response_data