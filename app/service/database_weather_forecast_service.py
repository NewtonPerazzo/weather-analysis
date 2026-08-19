from app.dependencies import get_connection_handler
from app.entity.weather_forecast_database_entity import (
    WeatherForecastDatabaseEntity,
)
from app.model.city_info_model import ForecastResponseModel
from app.repository.weather_forecast_database_repository import (
    DatabaseWeatherForecastRepository,
)


class DatabaseWeatherForecastService():
    def __init__(
        self,
    ) -> None:
        self.__weather_forecast_repository = DatabaseWeatherForecastRepository(
            connection_handler_factory=get_connection_handler,
        )

    def get_forecast(
        self,
        city_id: str,
        forecast_days: int,
    ) -> ForecastResponseModel | None:

        forecast = self.__weather_forecast_repository.get_forecast(
            city_id=city_id,
            forecast_days=forecast_days,
        )

        if not forecast:
            return None

        return ForecastResponseModel.model_validate(
            forecast.forecast_data
        )

    def add_forecast(
        self,
        city_id: str,
        forecast_days: int,
        forecast: ForecastResponseModel,
    ) -> WeatherForecastDatabaseEntity:

        return self.__weather_forecast_repository.add_forecast(
            city_id=city_id,
            forecast_days=forecast_days,
            forecast=forecast,
        )

    def delete_expired_forecasts(self) -> None:
        self.__weather_forecast_repository.delete_expired_forecasts()

database_weather_forecast_service = DatabaseWeatherForecastService()