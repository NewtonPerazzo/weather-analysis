from fastapi import APIRouter, HTTPException
from app.service.integration_weather_service import integration_weather_service
from app.model.city_info_model import ForecastResponseModel


open_meteo_router = APIRouter(
    prefix="",
    tags=["Open Meteo Info"]
)

@open_meteo_router.get(
    "/search-city",
)
async def get_forecast(
    name: str,
    country_code: str,
    count: int = 1,
    language: str = 'en',
    format: str = 'json',
    forecast_days: int = 1
) -> ForecastResponseModel:

    response = await integration_weather_service.get_city_forecast_info(
        name=name, 
        country_code=country_code,
        count=count,
        language=language,
        format=format,
        forecast_days=forecast_days
    )
    return response