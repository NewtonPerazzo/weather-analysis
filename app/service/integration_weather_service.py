from json import JSONDecodeError
from typing import TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from app.exceptions.exceptions import (
    CityNotFoundException,
    InvalidWeatherProviderResponseException,
)
from app.model.city_info_model import CityForecastInfoParams, CityInfoModel, CityInfoParams, CityInfoResponseModel, ForecastResponseModel
from config.settings import get_settings
from app.dependencies import get_open_meteo_integration


ResponseModel = TypeVar("ResponseModel", bound=BaseModel)

class IntegrationWeatherService():
    def __init__(self) -> None:
        settings = get_settings()
        self.__open_meteo_integration = get_open_meteo_integration(settings)

    async def get_city_info(
        self,
        name: str,
        country_code: str,
        count: int = 1,
        language: str = 'en',
        format: str = 'json'
    ) -> CityInfoModel:
        params: CityInfoParams = {
            "name": name,
            "count": count,
            "language": language,
            "countryCode": country_code,
            "format": format
        }

        response = await self.__open_meteo_integration.get_city_info(params=params)

        city_info = self.__validate_provider_response(
            response=response,
            response_model=CityInfoResponseModel,
        )

        if not city_info.results:
            raise CityNotFoundException(name)

        return city_info.results[0]
        
    async def get_city_forecast_info(
        self,
        name: str,
        country_code: str,
        count: int = 1,
        language: str = 'en',
        format: str = 'json',
        forecast_days: int = 1
    ) -> ForecastResponseModel:
        city = await self.get_city_info(
            name=name,
            country_code=country_code,
            count=count,
            language=language,
            format=format
        )
        
        params: CityForecastInfoParams = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "forecast_days": forecast_days,
            "timezone": city.timezone,

            "current": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "weather_code",
                "wind_speed_10m",
            ]),

            "hourly": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation_probability",
                "precipitation",
                "weather_code",
                "wind_speed_10m",
            ]),

            "daily": ",".join([
                "temperature_2m_max",
                "temperature_2m_min",
                "apparent_temperature_max",
                "apparent_temperature_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "weather_code",
                "sunrise",
                "sunset",
            ]),
        }

        response = await self.__open_meteo_integration.get_city_forecast_info(params=params)

        forecast = self.__validate_provider_response(
            response=response,
            response_model=ForecastResponseModel,
        )
        return forecast

    def __validate_provider_response(
        self,
        response: httpx.Response,
        response_model: type[ResponseModel],
    ) -> ResponseModel:
        try:
            response_data = response.json()
        except (JSONDecodeError, UnicodeDecodeError) as error:
            raise InvalidWeatherProviderResponseException() from error

        try:
            return response_model.model_validate(response_data)
        except ValidationError as error:
            raise InvalidWeatherProviderResponseException() from error

integration_weather_service = IntegrationWeatherService()
