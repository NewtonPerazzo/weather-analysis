from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    CityInfoAlreadyExistsInDBException,
    CityNotFoundException,
    ForecastDateUnavailableException,
    InvalidWeatherProviderResponseException,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CityNotFoundException)
    async def city_not_found_handler(
        request: Request,
        exception: CityNotFoundException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "error": "city_not_found",
                "message": str(exception),
            },
        )

    @app.exception_handler(ForecastDateUnavailableException)
    async def forecast_date_unavailable_handler(
        request: Request,
        exception: ForecastDateUnavailableException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": "forecast_date_unavailable",
                "message": str(exception),
            },
        )

    @app.exception_handler(InvalidWeatherProviderResponseException)
    async def invalid_weather_provider_response_handler(
        request: Request,
        exception: InvalidWeatherProviderResponseException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=502,
            content={
                "error": "invalid_weather_provider_response",
                "message": str(exception),
            },
        )

    @app.exception_handler(CityInfoAlreadyExistsInDBException)
    async def city_info_already_exists_in_db_handler(
        request: Request,
        exception: CityInfoAlreadyExistsInDBException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "error": "city_info_already_exists_in_db",
                "message": str(exception),
            },
        )
