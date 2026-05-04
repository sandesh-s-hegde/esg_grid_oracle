from services.esg_client import fetch_carbon_intensity
from services import esg_client


def test_esg_client_fallback_on_failure():
    """Ensure the client returns a safe fallback if the Oracle is unreachable."""
    esg_client.ESG_ORACLE_URL = "http://localhost:9999"

    result = fetch_carbon_intensity("FR")

    assert result["grid_status"] == "UNKNOWN"
    assert result["intensity_gco2_kwh"] == 0