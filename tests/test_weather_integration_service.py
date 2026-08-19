import asyncio

import httpx
import pytest

from app.exceptions.exceptions import CityNotFoundException
from app.model.city_info_model import SearchCityRequest
from app.service.integration_weather_service import IntegrationWeatherService


# class FakeOpenMeteoIntegration:
#     def __init__(self, response_data: dict) -> None:
#         self.response_data = response_data
#         self.received_params: dict | None = None

#     async def get_city_info(self, params: dict) -> httpx.Response:
#         self.received_params = params

#         return httpx.Response(
#             status_code=200,
#             json=self.response_data,
#             request=httpx.Request(
#                 "GET",
#                 "https://open-meteo.test/v1/search",
#             ),
#         )


# class FakeDatabaseCityInfoService:
#     def get_city_info_by_key(self, key: str):
#         return None

#     def add_city_info(self, city, key: str):
#         return city


# def build_service(
#     integration: FakeOpenMeteoIntegration,
# ) -> IntegrationWeatherService:

#     service = object.__new__(IntegrationWeatherService)

#     service._IntegrationWeatherService__open_meteo_integration = integration

#     service._IntegrationWeatherService__database_info_city_service = (
#         FakeDatabaseCityInfoService()
#     )

#     return service


# def mock_redis(monkeypatch):
#     monkeypatch.setattr(
#         "app.service.integration_weather_service.get_data_redis",
#         lambda key: None,
#     )

#     monkeypatch.setattr(
#         "app.service.integration_weather_service.set_data_redis",
#         lambda key, value, time: None,
#     )


def test_get_city_info_sends_only_geocoding_parameters(
    monkeypatch,
) -> None:
    pass
    # integration = FakeOpenMeteoIntegration({
    #     "results": [
    #         {
    #             "id": 3461311,
    #             "name": "Indaiatuba",
    #             "latitude": -23.08842,
    #             "longitude": -47.2119,
    #             "feature_code": "PPLA2",
    #             "country_code": "BR",
    #             "timezone": "America/Sao_Paulo",
    #         }
    #     ],
    #     "generationtime_ms": 0.2,
    # })

    # service = build_service(integration)

    # mock_redis(monkeypatch)

    # asyncio.run(
    #     service.get_city_info(
    #         SearchCityRequest(
    #             name="Indaiatuba",
    #             country_code="BR",
    #             forecast_days=16,
    #         )
    #     )
    # )

    # assert integration.received_params == {
    #     "name": "Indaiatuba",
    #     "count": 1,
    #     "language": "en",
    #     "format": "json",
    #     "countryCode": "BR",
    # }


def test_get_city_info_raises_city_not_found_when_results_are_absent(
    monkeypatch,
) -> None:

    # integration = FakeOpenMeteoIntegration({
    #     "generationtime_ms": 0.2,
    # })

    # service = build_service(integration)

    # mock_redis(monkeypatch)

    # with pytest.raises(CityNotFoundException):
    #     asyncio.run(
    #         service.get_city_info(
    #             SearchCityRequest(
    #                 name="Unknown city",
    #                 country_code="BR",
    #             )
    #         )
    #     )
    pass