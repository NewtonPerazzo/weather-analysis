from app.service.integration_weather_service import integration_weather_service
from datetime import datetime
from typing import cast
from app.model.city_analysis_model import CityForecastAnalysisResponseModel, CityHourAnalysisData, CityHourAnalysisResponseModel, CityHourAnalysisInfo, ScoreResponseModel
from app.model.city_info_model import CurrentWeatherModel, ForecastResponseModel, HourlyWeatherModel
from app.util.score import calculate_weather_score

class AnalysisWeatherService():
    def __init__(self) -> None:
        self._integration_weather_service = integration_weather_service

    async def get_forecast_analysis(
            self,  
            city: str, 
            country_code: str, 
        ) -> CityForecastAnalysisResponseModel:

        city_forecast = await self._integration_weather_service.get_city_forecast_info(
            name=city,
            country_code=country_code
        )
        max_temperature = max(city_forecast.hourly.temperature_2m)
        min_temperature = min(city_forecast.hourly.temperature_2m)

        max_temperature_index = city_forecast.hourly.temperature_2m.index(max_temperature)
        min_temperature_index = city_forecast.hourly.temperature_2m.index(min_temperature)

        max_temperature_hour = datetime.fromisoformat(
            city_forecast.hourly.time[max_temperature_index])\
            .time()\
            .strftime('%H:%M')
        
        min_temperature_hour = datetime.fromisoformat(
            city_forecast.hourly.time[min_temperature_index])\
            .time()\
            .strftime('%H:%M')

        rain_probabily_max_temperature = city_forecast.hourly.precipitation_probability[max_temperature_index]
        rain_probabily_min_temperature = city_forecast.hourly.precipitation_probability[min_temperature_index]

        
        return CityForecastAnalysisResponseModel(
            current_temperature=city_forecast.current.temperature_2m,
            current_hour=datetime.fromisoformat(city_forecast.current.time).time().strftime('%H:%M'),
            max_temperature=max_temperature,
            max_temperature_hour=max_temperature_hour,
            min_temperature=min_temperature,
            min_temperature_hour=min_temperature_hour,
            rain_probabily_max_temperature=rain_probabily_max_temperature,
            rain_probabily_min_temperature=rain_probabily_min_temperature,
        )

    async def get_forecast_hour_analysis(self, city: str, country_code: str, day: str = None) -> CityHourAnalysisResponseModel:
        city_forecast = await self._integration_weather_service.get_city_forecast_info(
            name=city,
            country_code=country_code,
            forecast_days= 1 if not day else 16
        )

        city_forecast_hourly = city_forecast.hourly

        current_hour = None if day else self.get_hourly_score_info_current(city_forecast.current)

        if day:
              city_forecast_hourly = self.get_hourly_score_info_other_day(city_forecast, day)


        hours = self.get_hourly_score_info_list(city_forecast_hourly)

        return CityHourAnalysisResponseModel(
            current_hour=current_hour,
            hours=hours,
        )

    def get_hourly_score_info_other_day(self, city_forecast: ForecastResponseModel, day: str) -> CityHourAnalysisData:
        city_forecast_hourly = HourlyWeatherModel(
            time=[],
            temperature_2m=[],
            relative_humidity_2m=[],
            apparent_temperature=[],
            precipitation_probability=[],
            precipitation=[],
            weather_code=[],
            wind_speed_10m=[]
        )

        for i in range(len(city_forecast.hourly.time)):
            requested_date = datetime.fromisoformat(day).date()
            forecast_date = datetime.fromisoformat(
                city_forecast.hourly.time[i]
            ).date()

            if forecast_date == requested_date:
                city_forecast_hourly.time.append(city_forecast.hourly.time[i])
                city_forecast_hourly.temperature_2m.append(city_forecast.hourly.temperature_2m[i])
                city_forecast_hourly.relative_humidity_2m.append(city_forecast.hourly.relative_humidity_2m[i])
                city_forecast_hourly.apparent_temperature.append(city_forecast.hourly.apparent_temperature[i])
                city_forecast_hourly.precipitation_probability.append(city_forecast.hourly.precipitation_probability[i])
                city_forecast_hourly.precipitation.append(city_forecast.hourly.precipitation[i])
                city_forecast_hourly.weather_code.append(city_forecast.hourly.weather_code[i])
                city_forecast_hourly.wind_speed_10m.append(city_forecast.hourly.wind_speed_10m[i])

        return city_forecast_hourly  
        
    def get_hourly_score_info_current(self, current: CurrentWeatherModel | None) -> CityHourAnalysisData:
        if not current:return None
        current_temperature = cast(float, current.temperature_2m)
        current_rain_probability = cast(float, current.precipitation)
        current_wind_speed = cast(float, current.wind_speed_10m)
        current_humidity = cast(int, current.relative_humidity_2m)
        current_apparent_temperature = cast(float, current.apparent_temperature)

        result: ScoreResponseModel = calculate_weather_score(
            temperature=current_temperature,
            rain_probability=current_rain_probability,
            wind_speed=current_wind_speed,
            humidity=current_humidity,
        )

        return CityHourAnalysisData(
            hour=datetime.fromisoformat(current.time).time().strftime('%H:%M'),
            score=result.score,
            reason=result.reasons,
            info=CityHourAnalysisInfo(
                temperature=current_temperature,
                rain_probability=current_rain_probability,
                wind_speed=current_wind_speed,
                humidity=current_humidity,
                apparent_temperature=current_apparent_temperature,
            )
        )
    
    
    def get_hourly_score_info_list(self, hourly_list: HourlyWeatherModel) -> list[CityHourAnalysisData]:
        response: list[CityHourAnalysisData] = []

        for i in range(len(hourly_list.time)):
            hour = hourly_list.time[i]
            temperature = cast(float, hourly_list.temperature_2m[i])
            rain_probability = cast(float, hourly_list.precipitation[i])
            wind_speed = cast(float, hourly_list.wind_speed_10m[i])
            humidity = cast(int, hourly_list.relative_humidity_2m[i])
            apparent_temperature = cast(float, hourly_list.apparent_temperature[i])

            result: ScoreResponseModel = calculate_weather_score(
                temperature=temperature,
                rain_probability=rain_probability,
                wind_speed=wind_speed,
                humidity=humidity,
            )

            response.append(CityHourAnalysisData(
                hour=datetime.fromisoformat(hour).time().strftime('%H:%M'),
                score=result.score,
                reason=result.reasons,
                info=CityHourAnalysisInfo(
                    temperature=temperature,
                    rain_probability=rain_probability,
                    wind_speed=wind_speed,
                    humidity=humidity,
                    apparent_temperature=apparent_temperature
                )
            ))
        
        return response

analysis_weather_service = AnalysisWeatherService()
