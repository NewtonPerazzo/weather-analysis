from fastapi import APIRouter
from app.service.analysis_weather_service import analysis_weather_service
from app.model.city_analysis_model import CityForecastAnalysisResponseModel, CityHourAnalysisResponseModel


analysis_router = APIRouter(
    prefix="",
    tags=["Analysis Weather Info"]
)

@analysis_router.get(
    "/get-forecast-analysis",
)
async def get_forecast_analysis(
    city: str, 
    country_code: str,
) -> CityForecastAnalysisResponseModel:
    
    response = await analysis_weather_service.get_forecast_analysis(
        city=city, 
        country_code=country_code,
    )
    return response

@analysis_router.get(
    "/get-forecast-hourly-analysis",
)
async def get_forecast_hour_analysis(
    city: str, 
    country_code: str,
    day: str = None
) -> CityHourAnalysisResponseModel:
    
    response = await analysis_weather_service.get_forecast_hour_analysis(
        city=city, 
        country_code=country_code,
        day=day
    )
    return response