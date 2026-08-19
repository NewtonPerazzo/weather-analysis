from datetime import datetime, timedelta, timezone
from typing import Callable

from app.dependencies import get_connection_handler
from app.entity.weather_forecast_database_entity import (
    WeatherForecastDatabaseEntity,
)
from app.model.city_info_model import ForecastResponseModel
from config.db_connection import DBConnectionHandler


class DatabaseWeatherForecastRepository():
    def __init__(
            self,
            connection_handler_factory: Callable[[], DBConnectionHandler],
        ) -> None:
            self.__connection_handler_factory = connection_handler_factory
        
    def get_forecast(
        self,
        city_id: str,
        forecast_days: int,
    ) -> ForecastResponseModel | None:
        with self.__connection_handler_factory() as db:
            forecast = (
                db.session
                .query(WeatherForecastDatabaseEntity)
                .filter(
                    WeatherForecastDatabaseEntity.city_id == city_id,
                    WeatherForecastDatabaseEntity.forecast_days == forecast_days,
                    WeatherForecastDatabaseEntity.expires_at
                    > datetime.now(timezone.utc),
                )
                .first()
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
        now = datetime.now(timezone.utc)
        with self.__connection_handler_factory() as db:

            forecast_entity = WeatherForecastDatabaseEntity(
                city_id=city_id,
                forecast_days=forecast_days,
                forecast_data=forecast.model_dump(mode="json"),
                created_at=now,
                expires_at=now + timedelta(hours=1),
            )

            db.session.add(forecast_entity)
            db.session.commit()
            db.session.refresh(forecast_entity)

            return forecast_entity

    def delete_expired_forecasts(self) -> None:
        with self.__connection_handler_factory() as db:
            db.session.query(
                WeatherForecastDatabaseEntity
            ).filter(
                WeatherForecastDatabaseEntity.expires_at
                < datetime.now(timezone.utc)
            ).delete(
                synchronize_session=False
            )

            db.session.commit()