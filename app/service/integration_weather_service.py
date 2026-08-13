from json import JSONDecodeError
from typing import TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from app.exceptions.exceptions import (
    CityNotFoundException,
    InvalidWeatherProviderResponseException,
)
from app.model.city_info_model import CityForecastInfoParams, CityInfoModel, CityInfoParams, CityInfoResponseModel, ForecastResponseModel, SearchCityRequest
from config.settings import get_settings
from app.dependencies import get_open_meteo_integration


ResponseModel = TypeVar("ResponseModel", bound=BaseModel)

class IntegrationWeatherService():
    def __init__(self) -> None:
        settings = get_settings()
        self.__open_meteo_integration = get_open_meteo_integration(settings)

    async def get_city_info(
        self,
        city_request: SearchCityRequest
    ) -> CityInfoModel:
        params: CityInfoParams = {
            "name": city_request.name,
            "count": city_request.count,
            "language": city_request.language,
            "format": city_request.format,
            "countryCode": city_request.country_code,
        }

        response = await self.__open_meteo_integration.get_city_info(params=params)

        city_info = self.__validate_provider_response(
            response=response,
            response_model=CityInfoResponseModel,
        )

        if not city_info.results:
            raise CityNotFoundException(city_name=city_request.name)

        return city_info.results[0]
        
    async def get_city_forecast_info(
        self,
        city_request: SearchCityRequest
    ) -> ForecastResponseModel:
        city = await self.get_city_info(city_request=city_request)
        
        params: CityForecastInfoParams = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "forecast_days": city_request.forecast_days,
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
