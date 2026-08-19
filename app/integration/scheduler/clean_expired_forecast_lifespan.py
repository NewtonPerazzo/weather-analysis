from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.service.database_city_info_service import data_base_info_service

@asynccontextmanager
async def clean_expire_forecast_lifespan(app: FastAPI):
    data_base_info_service.delete_city_info_expired()
    yield