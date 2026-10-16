import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    CityInfoAlreadyExistsInDBException,
    CityNotFoundException,
    ForecastDateUnavailableException,
    InvalidWeatherProviderResponseException,
)


logger = logging.getLogger(__name__)


def error_response(status_code: int, error: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": error, "message": message},
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CityNotFoundException)
    async def city_not_found_handler(
        request: Request,
        exception: CityNotFoundException,
    ) -> JSONResponse:
        return error_response(
            status_code=404,
            error="city_not_found",
            message="The requested city could not be found.",
        )

    @app.exception_handler(ForecastDateUnavailableException)
    async def forecast_date_unavailable_handler(
        request: Request,
        exception: ForecastDateUnavailableException,
    ) -> JSONResponse:
        return error_response(
            status_code=422,
            error="forecast_date_unavailable",
            message="The selected date is outside the available forecast period.",
        )

    @app.exception_handler(InvalidWeatherProviderResponseException)
    async def invalid_weather_provider_response_handler(
        request: Request,
        exception: InvalidWeatherProviderResponseException,
    ) -> JSONResponse:
        return error_response(
            status_code=502,
            error="weather_provider_unavailable",
            message="Weather information is temporarily unavailable.",
        )

    @app.exception_handler(CityInfoAlreadyExistsInDBException)
    async def city_info_already_exists_in_db_handler(
        request: Request,
        exception: CityInfoAlreadyExistsInDBException,
    ) -> JSONResponse:
        return error_response(
            status_code=400,
            error="city_info_already_exists",
            message="This city information is already available.",
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(
        request: Request,
        exception: RequestValidationError,
    ) -> JSONResponse:
        return error_response(
            status_code=422,
            error="invalid_request",
            message="Please review the information and try again.",
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exception: HTTPException,
    ) -> JSONResponse:
        error_by_status = {
            400: "invalid_request",
            404: "resource_not_found",
            422: "invalid_request",
        }
        error = error_by_status.get(exception.status_code, "request_failed")
        return error_response(
            status_code=exception.status_code,
            error=error,
            message="We could not complete this request right now.",
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exception: Exception,
    ) -> JSONResponse:
        logger.exception("Unhandled weather-analysis error")
        return error_response(
            status_code=500,
            error="internal_error",
            message="We could not complete this request right now.",
        )
