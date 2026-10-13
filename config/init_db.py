from config.base import Base
from config.db_connection import DBConnectionHandler
from config.settings import get_settings

# import entities for register my table on metadata
from app.entity.city_info_database_entity import CityInfoDatabaseEntity
from app.entity.weather_forecast_database_entity import WeatherForecastDatabaseEntity


def init_db() -> None:
    settings = get_settings()

    db = DBConnectionHandler(settings.database_url)

    Base.metadata.create_all(bind=db.get_engine())

    print("Database tables initialized successfully")


if __name__ == "__main__":
    init_db()