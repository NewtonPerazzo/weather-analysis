from typing import TypedDict

from pydantic import BaseModel, ConfigDict

class SearchCityRequest(BaseModel):
    name: str
    country_code: str
    count: int = 1
    language: str = 'en'
    format: str = 'json'
    forecast_days: int = 1

class CityInfoModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    latitude: float
    longitude: float
    elevation: float | None = None
    feature_code: str
    country_code: str
    timezone: str
    population: int | None = None
    country: str | None = None
    admin1: str | None = None


class CityInfoResponseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    results: list[CityInfoModel]
    generationtime_ms: float


class CurrentWeatherUnitsModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    time: str
    interval: str
    temperature_2m: str
    relative_humidity_2m: str
    apparent_temperature: str
    precipitation: str
    weather_code: str
    wind_speed_10m: str


class CurrentWeatherModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    time: str
    interval: int
    temperature_2m: float | None
    relative_humidity_2m: int | None
    apparent_temperature: float | None
    precipitation: float | None
    weather_code: int | None
    wind_speed_10m: float | None


class HourlyWeatherUnitsModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    time: str
    temperature_2m: str
    relative_humidity_2m: str
    apparent_temperature: str
    precipitation_probability: str
    precipitation: str
    weather_code: str
    wind_speed_10m: str


class HourlyWeatherModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    time: list[str]
    temperature_2m: list[float | None]
    relative_humidity_2m: list[int | None]
    apparent_temperature: list[float | None]
    precipitation_probability: list[int | None]
    precipitation: list[float | None]
    weather_code: list[int | None]
    wind_speed_10m: list[float | None]


class DailyWeatherUnitsModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    time: str
    temperature_2m_max: str
    temperature_2m_min: str
    apparent_temperature_max: str
    apparent_temperature_min: str
    precipitation_sum: str
    precipitation_probability_max: str
    weather_code: str
    sunrise: str
    sunset: str


class DailyWeatherModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    time: list[str]
    temperature_2m_max: list[float | None]
    temperature_2m_min: list[float | None]
    apparent_temperature_max: list[float | None]
    apparent_temperature_min: list[float | None]
    precipitation_sum: list[float | None]
    precipitation_probability_max: list[int | None]
    weather_code: list[int | None]
    sunrise: list[str]
    sunset: list[str]


class ForecastResponseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    current_units: CurrentWeatherUnitsModel
    current: CurrentWeatherModel
    hourly_units: HourlyWeatherUnitsModel
    hourly: HourlyWeatherModel
    daily_units: DailyWeatherUnitsModel
    daily: DailyWeatherModel

class CityInfoParams(TypedDict):
    name: str
    count: int
    language: str
    countryCode: str
    format: str


class CityForecastInfoParams(TypedDict):
    latitude: float
    longitude: float
    forecast_days: int
    timezone: str
    current: str
    hourly: str
    daily: str
