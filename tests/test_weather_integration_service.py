import asyncio

import httpx
import pytest

from app.exceptions.exceptions import CityNotFoundException
from app.model.city_info_model import SearchCityRequest
from app.service.integration_weather_service import IntegrationWeatherService
import app.service.integration_weather_service as weather_service_module


@pytest.fixture(autouse=True)
def fake_redis_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(weather_service_module, "get_data_redis", lambda key: None)
    monkeypatch.setattr(weather_service_module, "set_data_redis", lambda key, value, time: None)


class FakeOpenMeteoIntegration:
    def __init__(self, response_data: dict) -> None:
        self.response_data = response_data
        self.received_params: dict | None = None

    async def get_city_info(self, params: dict) -> httpx.Response:
        self.received_params = params
        return httpx.Response(
            status_code=200,
            json=self.response_data,
            request=httpx.Request("GET", "https://open-meteo.test/v1/search"),
        )


def build_service(integration: FakeOpenMeteoIntegration) -> IntegrationWeatherService:
    service = object.__new__(IntegrationWeatherService)
    service._IntegrationWeatherService__open_meteo_integration = integration
    return service


def test_get_city_info_sends_only_geocoding_parameters() -> None:
    integration = FakeOpenMeteoIntegration({
        "results": [{
            "id": 3461311,
            "name": "Indaiatuba",
            "latitude": -23.08842,
            "longitude": -47.2119,
            "feature_code": "PPLA2",
            "country_code": "BR",
            "timezone": "America/Sao_Paulo",
        }],
        "generationtime_ms": 0.2,
    })
    service = build_service(integration)

    asyncio.run(service.get_city_info(SearchCityRequest(
        name="Indaiatuba",
        country_code="BR",
        forecast_days=16,
    )))

    assert integration.received_params == {
        "name": "Indaiatuba",
        "count": 1,
        "language": "en",
        "format": "json",
        "countryCode": "BR",
    }


def test_get_city_info_raises_city_not_found_when_results_are_absent() -> None:
    integration = FakeOpenMeteoIntegration({"generationtime_ms": 0.2})
    service = build_service(integration)

    with pytest.raises(CityNotFoundException):
        asyncio.run(service.get_city_info(SearchCityRequest(
            name="Unknown city",
            country_code="BR",
        )))
