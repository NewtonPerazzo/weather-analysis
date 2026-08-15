from typing import Literal

from pydantic import BaseModel

class CityForecastAnalysisResponseModel(BaseModel):
    current_temperature: float
    current_hour: str
    max_temperature: float
    max_temperature_hour: str
    min_temperature: float
    min_temperature_hour: str
    rain_probabily_max_temperature: int
    rain_probabily_min_temperature: int

class CityHourAnalysisInfo(BaseModel):
    temperature: float
    rain_probability: float
    wind_speed: float
    humidity: int
    apparent_temperature: float

class CityHourAnalysisData(BaseModel):
    hour: str
    score: int
    reason: list[str]
    info: CityHourAnalysisInfo

class CityHourAnalysisResponseModel(BaseModel):
    current_hour: CityHourAnalysisData | None
    hours: list[CityHourAnalysisData]

class ScoreResponseModel(BaseModel):
    score: int
    reasons: list[str]

FilterTime = Literal["morning", "night", "evening", "dawn"]
