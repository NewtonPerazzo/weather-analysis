from fastapi import APIRouter, HTTPException
from app.service.integration_weather_service import integration_weather_service
from app.model.city_info_model import ForecastResponseModel, SearchCityRequest


open_meteo_router = APIRouter(
    prefix="",
    tags=["Open Meteo Info"]
)

@open_meteo_router.post(
    "/search-city",
)
async def get_forecast(
    city_request: SearchCityRequest
) -> ForecastResponseModel:

    response = await integration_weather_service.get_city_forecast_info(city_request=city_request)
    return response