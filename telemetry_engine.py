import random
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] ESG_Oracle: %(message)s")
logger = logging.getLogger("CarbonOracle")


class CarbonIntensityAPI:
    """Simulates real-time grid carbon intensity (gCO2eq/kWh) for spatial energy arbitrage."""

    def __init__(self):
        self.supported_regions = {"DE", "FR", "IE", "UK", "NL"}

    def get_live_carbon_intensity(self, region: str) -> dict:
        if region not in self.supported_regions:
            logger.error(f"Region {region} is out of bounds.")
            return {"error": "Region not supported"}

        intensity_models = {
            "FR": random.randint(30, 60),
            "UK": random.randint(150, 250),
            "IE": random.randint(100, 300),
            "NL": random.randint(200, 400),
            "DE": random.randint(300, 500)
        }

        intensity = intensity_models.get(region, 250)

        if intensity < 150:
            status = "GREEN"
        elif intensity < 350:
            status = "AMBER"
        else:
            status = "RED"

        logger.info(f"Fetched Carbon Intensity for {region}: {intensity} gCO2eq/kWh [{status}]")

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "region": region,
            "intensity_gco2_kwh": intensity,
            "grid_status": status
        }


if __name__ == "__main__":
    oracle = CarbonIntensityAPI()
    oracle.get_live_carbon_intensity("FR")
    oracle.get_live_carbon_intensity("DE")
    oracle.get_live_carbon_intensity("IE")