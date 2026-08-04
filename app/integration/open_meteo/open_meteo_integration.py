import httpx
from app.model.city_info_model import CityForecastInfoParams, CityInfoParams


class OpenMeteoIntegration():
    def __init__(
            self, 
            open_meteo_url: str, 
            open_meteo_forecast_url: str,
            open_meteo_archive_url: str
        ):
        self.open_meteo_url = open_meteo_url
        self.open_meteo_forecast_url = open_meteo_forecast_url
        self.open_meteo_archive_url = open_meteo_archive_url
        self.open_meteo_search_city_uri = '/v1/search'
        self.open_meteo_forecast_uri = '/v1/forecast'
        self.open_meteo_archive_uri = '/v1/archive'

    async def get_city_info(
        self,
        params: CityInfoParams,
    ) -> httpx.Response:
        url = f"{self.open_meteo_url}{self.open_meteo_search_city_uri}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return response
        
    async def get_city_forecast_info(
        self,
        params: CityForecastInfoParams,
    ) -> httpx.Response:
        url = f"{self.open_meteo_forecast_url}{self.open_meteo_forecast_uri}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return response
