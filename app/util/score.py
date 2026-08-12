from app.model.city_analysis_model import ScoreResponseModel

SCORE_REASONS: dict[str, str] = {
    "high_temperature": "Temperature is too high",
    "low_temperature": "Temperature is too low",
    "high_rain_probability": "High probability of rain",
    "high_wind_speed": "Wind speed is too high",
    "high_humidity_and_high_temperature": "High humidity and temperature combination",
    "low_humidity": "Humidity is too low"
}

def calculate_weather_score(
    temperature: float,
    rain_probability: float,
    wind_speed: float,
    humidity: int,
) -> ScoreResponseModel:
    score = 10

    result = ScoreResponseModel(score=score, reasons=[])
        
    if temperature > 27:
        result.score -= 2
        result.reasons.append(SCORE_REASONS["high_temperature"])
    if temperature < 13:
        result.score -= 2
        result.reasons.append(SCORE_REASONS["low_temperature"])
    if rain_probability > 50:
        result.score -= 4
        result.reasons.append(SCORE_REASONS["high_rain_probability"])
    if wind_speed > 30:
        result.score -= 1
        result.reasons.append(SCORE_REASONS["high_wind_speed"])
    if temperature > 30 and humidity > 85:
        result.score -= 3
        result.reasons.append(SCORE_REASONS["high_humidity_and_high_temperature"])
    if humidity < 30:
        result.score -= 2
        result.reasons.append(SCORE_REASONS["low_humidity"])

    return result
