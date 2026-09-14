from app.spreadsheet.spreadsheet_generator import spreadsheet_generator
from config.celery import celery_app


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_spreadsheet_task(self, data: dict) -> dict:
    city_key = data.get("city_key", "unknown")
    city_name = data.get("city_name", city_key)
    hourly = data["hourly"]
    filters = data.get("filters", {})
    hourly_data = [
        {
            "time": hourly["time"][index],
            "temperature": hourly["temperature_2m"][index],
            "humidity": hourly["relative_humidity_2m"][index],
            "wind_speed": hourly["wind_speed_10m"][index],
            "weather_code": hourly["weather_code"][index],
        }
        for index in range(len(hourly["time"]))
    ]
    report_suffix = "_".join(
        value for value in (filters.get("day"), filters.get("period")) if value
    )
    report_name = f"weather_report_{city_key}{f'_{report_suffix}' if report_suffix else ''}.xlsx"
    file_path = spreadsheet_generator.create_spreadsheet(
        city_name=city_name,
        city_key=city_key,
        hourly_data=hourly_data,
        filters=filters,
        report_name=report_name,
    )
    return {
        "city_key": city_key,
        "file": file_path,
        "report": report_name,
        "status": "completed",
    }
