from typing import Annotated

from fastapi import Depends

from config.settings import Settings, get_settings
from app.integration.open_meteo.open_meteo_integration import OpenMeteoIntegration
from config.db_connection import DBConnectionHandler


def get_open_meteo_integration(
    settings: Annotated[Settings, Depends(get_settings)],
) -> OpenMeteoIntegration:
    return OpenMeteoIntegration(
        open_meteo_url = settings.open_meteo_url,
        open_meteo_forecast_url = settings.open_meteo_forecast_url,
        open_meteo_archive_url = settings.open_meteo_archive_url
    )

settings = get_settings()

connection_handler = DBConnectionHandler(
    connection_string=settings.database_url
)

OpenMeteoDependency = Annotated[
    OpenMeteoIntegration,
    Depends(get_open_meteo_integration),
]