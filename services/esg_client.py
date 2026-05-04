import os
import httpx
import logging

logger = logging.getLogger("CapacityOptimizer")
ESG_ORACLE_URL = os.getenv("ESG_ORACLE_URL", "http://localhost:8000")


async def fetch_carbon_intensity(region: str) -> dict:
    """Fetches real-time carbon telemetry from the ESG Oracle."""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{ESG_ORACLE_URL}/api/v1/carbon/{region}")
            response.raise_for_status()
            data = response.json()

            logger.info(
                f"ESG Oracle: {region} is currently {data.get('grid_status')} ({data.get('intensity_gco2_kwh')} gCO2/kWh)")
            return data

    except httpx.HTTPError as e:
        logger.error(f"Failed to reach ESG Oracle for region {region}: {str(e)}")
        return {"region": region, "grid_status": "UNKNOWN", "intensity_gco2_kwh": 0}