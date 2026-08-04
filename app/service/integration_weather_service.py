from fastapi import HTTPException
from app.model.city_info_model import CityInfoResponseModel, CityInfoModel, ForecastResponseModel, CityInfoModel
from config.settings import get_settings
from app.dependencies import get_open_meteo_integration

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
        params: CityInfoModel = {
            "name": name,
            "count": count,
            "language": language,
            "countryCode": country_code,
            "format": format
        }

        response = await self.__open_meteo_integration.get_city_info(params=params)

        if response.status_code == 404 or not response.json().get("results"):
            raise HTTPException(
                status_code=404,
                detail="City not found",
            )
        response.raise_for_status()
        city_info = CityInfoResponseModel.model_validate(response.json())
        return city_info.results[0]
        
    async def get_city_forecast_info(
        self,
        name: str,
        country_code: str,
        count: int = 1,
        language: str = 'en',
        format: str = 'json',
        forecast_days: int = 1
    ):
        city = await self.get_city_info(
            name=name,
            country_code=country_code,
            count=count,
            language=language,
            format=format
        )
        
        params = {
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
        response.raise_for_status()

        forecast = ForecastResponseModel.model_validate(response.json())
        return forecast

integration_weather_service = IntegrationWeatherService()