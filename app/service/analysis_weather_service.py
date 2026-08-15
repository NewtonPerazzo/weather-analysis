from app.exceptions.exceptions import ForecastDateUnavailableException, InvalidWeatherProviderResponseException
from app.service.integration_weather_service import integration_weather_service
from datetime import date, datetime, timedelta, time
from typing import cast
from app.model.city_analysis_model import CityForecastAnalysisResponseModel, CityHourAnalysisData, CityHourAnalysisResponseModel, CityHourAnalysisInfo, FilterTime, ScoreResponseModel
from app.model.city_info_model import CurrentWeatherModel, ForecastResponseModel, HourlyWeatherModel, SearchCityRequest
from app.util.score import calculate_weather_score

class AnalysisWeatherService():
    def __init__(self) -> None:
        self._integration_weather_service = integration_weather_service

    async def get_forecast_analysis(
            self,  
            city: str, 
            country_code: str, 
        ) -> CityForecastAnalysisResponseModel:

        city_search = SearchCityRequest(
            name=city,
            country_code=country_code
        )
        city_forecast = await self._integration_weather_service.get_city_forecast_info(city_request=city_search)

        self._validate_hourly_data(city_forecast.hourly)

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

    async def get_forecast_hour_analysis(
        self,
        city: str,
        country_code: str,
        filter_time: FilterTime | None,
        day: date | None = None,
    ) -> CityHourAnalysisResponseModel:
        city_search = SearchCityRequest(
            name=city,
            country_code=country_code,
            forecast_days= 1 if not day else 16
        )
        city_forecast = await self._integration_weather_service.get_city_forecast_info(city_request=city_search)

        self._validate_hourly_data(city_forecast.hourly)

        city_forecast_hourly = city_forecast.hourly

        current_hour = None if day else self.get_hourly_score_info_current(
            city_forecast.current,
            city_forecast.hourly
        )

        if day:
            if day < datetime.now().date() or day > datetime.now().date() + timedelta(days=15):
                raise ForecastDateUnavailableException(date=day)
            city_forecast_hourly = self.get_hourly_score_info_other_day(city_forecast, day)

        hours = self.get_hourly_score_info_list(city_forecast_hourly)
        new_hours: list[CityHourAnalysisData] = []
        if filter_time:
            new_hours = self._get_filtered_hours(hours=hours, filter_time=filter_time)
            if current_hour:
                is_in_filter_range = self._get_is_filter_ranger(current_hour.hour, filter_time)

                if not is_in_filter_range:
                    current_hour = None

        return CityHourAnalysisResponseModel(
            current_hour=current_hour,
            hours=new_hours if filter_time else hours
        )

    def get_hourly_score_info_current(
        self,
        current: CurrentWeatherModel,
        hourly: HourlyWeatherModel,
    ) -> CityHourAnalysisData:
        current_temperature = cast(float, current.temperature_2m)
        current_datetime = datetime.fromisoformat(current.time)
        current_hour_index = next(
            index
            for index, hourly_time in enumerate(hourly.time)
            if datetime.fromisoformat(hourly_time).date() == current_datetime.date()
            and datetime.fromisoformat(hourly_time).hour == current_datetime.hour
        )
        current_rain_probability = cast(
            float,
            hourly.precipitation_probability[current_hour_index],
        )
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
            rain_probability = cast(
                float,
                hourly_list.precipitation_probability[i],
            )
            wind_speed = cast(float, hourly_list.wind_speed_10m[i])
            humidity = cast(int, hourly_list.relative_humidity_2m[i])
            apparent_temperature = cast(float, hourly_list.apparent_temperature[i])

            result: ScoreResponseModel = calculate_weather_score(
                temperature=temperature,
                rain_probability=rain_probability,
                wind_speed=wind_speed,
                humidity=humidity,
            )

            response.append(
                CityHourAnalysisData(
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
                )
            )
        
        return response

    def get_hourly_score_info_other_day(
        self,
        city_forecast: ForecastResponseModel,
        day: date,
    ) -> HourlyWeatherModel:
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
            forecast_date = datetime.fromisoformat(
                city_forecast.hourly.time[i]
            ).date()

            if forecast_date == day:
                hourly_time = city_forecast.hourly.time[i]
                hourly_temperature_2m = city_forecast.hourly.temperature_2m[i]
                hourly_relative_humidity_2m = city_forecast.hourly.relative_humidity_2m[i]
                hourly_precipitation = city_forecast.hourly.precipitation[i]
                hourly_weather_code = city_forecast.hourly.weather_code[i]
                hourly_wind_speed_10m = city_forecast.hourly.wind_speed_10m[i]

                city_forecast_hourly.time.append(hourly_time)
                city_forecast_hourly.temperature_2m.append(hourly_temperature_2m)
                city_forecast_hourly.relative_humidity_2m.append(hourly_relative_humidity_2m)
                city_forecast_hourly.apparent_temperature.append(city_forecast.hourly.apparent_temperature[i])
                city_forecast_hourly.precipitation_probability.append(city_forecast.hourly.precipitation_probability[i])
                city_forecast_hourly.precipitation.append(hourly_precipitation)
                city_forecast_hourly.weather_code.append(hourly_weather_code)
                city_forecast_hourly.wind_speed_10m.append(hourly_wind_speed_10m)

        return city_forecast_hourly  

    def _get_filtered_hours(self, filter_time: FilterTime, hours: list[CityHourAnalysisData]) -> list[CityHourAnalysisData]:
        filtered_hours: list[CityHourAnalysisData] = []
        for hour in hours:
            is_in_filter_range = self._get_is_filter_ranger(hour.hour, filter_time) 

            if is_in_filter_range:
                filtered_hours.append(hour)
        return filtered_hours

    def _get_is_filter_ranger(self, hour: str, filter_time: FilterTime) -> bool:
        time_hour = datetime.strptime(hour, "%H:%M").time()
        filter_range = self._get_time_interval(filter_time)
        is_in_filter_range = time_hour >= filter_range[0] and time_hour <= filter_range[1]

        return is_in_filter_range
    
    def _get_time_interval(self, time_hour: FilterTime) -> tuple[time, time]:
        match time_hour:
            case 'morning':
                return [time(5, 0, 0), time(11, 59, 59)]
            case 'evening':
                return [time(12, 00, 00), time(17, 59, 00)]
            case 'night':
                return [time(18, 00, 00), time(23, 59, 00)]
            case 'dawn':
                return [time(00,00, 00), time(4, 59, 00)]

    def _validate_hourly_data(self, hourly: HourlyWeatherModel) -> None:
        list_lengths = {
            len(hourly.time),
            len(hourly.temperature_2m),
            len(hourly.relative_humidity_2m),
            len(hourly.apparent_temperature),
            len(hourly.precipitation_probability),
            len(hourly.precipitation),
            len(hourly.weather_code),
            len(hourly.wind_speed_10m),
        }

        if 0 in list_lengths or len(list_lengths) != 1:
            raise InvalidWeatherProviderResponseException()
        
analysis_weather_service = AnalysisWeatherService()
